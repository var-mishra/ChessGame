import json
import os
import time
import requests

NIFI_API_URL = os.environ.get("NIFI_API_URL", "http://nifi:8080/nifi-api")
KAFKA_BOOTSTRAP = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
S3_ENDPOINT = os.environ["S3_ENDPOINT"]
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
ELASTIC_URL = os.environ["ELASTIC_URL"]

s = requests.Session()
s.headers.update({"Content-Type": "application/json"})

def wait_for_nifi():
    for _ in range(120):
        try:
            r = s.get(f"{NIFI_API_URL}/flow/status")
            if r.ok:
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError("NiFi API not ready")


def get_root_pg_id():
    r = s.get(f"{NIFI_API_URL}/flow/process-groups/root")
    r.raise_for_status()
    return r.json()["processGroupFlow"]["id"]


def create_processor(pg_id, type_, name, position, properties):
    payload = {
        "component": {
            "type": type_,
            "name": name,
            "position": position,
            "config": {
                "properties": properties
            }
        },
        "revision": {"version": 0},
        "disconnectedNodeAcknowledged": True
    }
    r = s.post(f"{NIFI_API_URL}/process-groups/{pg_id}/processors", data=json.dumps(payload))
    r.raise_for_status()
    return r.json()["id"], r.json()["component"].get("relationships", [])


def create_connection(pg_id, source_id, dest_id, relationships=None):
    payload = {
        "component": {
            "source": {"id": source_id, "type": "PROCESSOR"},
            "destination": {"id": dest_id, "type": "PROCESSOR"},
            "selectedRelationships": relationships or []
        },
        "revision": {"version": 0},
        "disconnectedNodeAcknowledged": True
    }
    r = s.post(f"{NIFI_API_URL}/process-groups/{pg_id}/connections", data=json.dumps(payload))
    r.raise_for_status()
    return r.json()["id"]


def start_processor(proc_id):
    payload = {
        "id": proc_id,
        "state": "RUNNING",
        "disconnectedNodeAcknowledged": True
    }
    r = s.put(f"{NIFI_API_URL}/processors/{proc_id}/run-status", data=json.dumps(payload))
    r.raise_for_status()


def main():
    wait_for_nifi()
    root_pg = get_root_pg_id()

    # Consume from Kafka (raw JSON flowfile content)
    consume_id, _ = create_processor(
        root_pg,
        "org.apache.nifi.processors.kafka.pubsub.ConsumeKafka_2_0",
        "Consume Kafka",
        {"x": 0.0, "y": 0.0},
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "topic": KAFKA_TOPIC,
            "group.id": "nifi-consumer",
            "honor.timestamps": "true",
            "auto.offset.reset": "earliest"
        }
    )

    # Send to S3
    puts3_id, _ = create_processor(
        root_pg,
        "org.apache.nifi.processors.aws.s3.PutS3Object",
        "Put to S3",
        {"x": 500.0, "y": 150.0},
        {
            "Bucket": S3_BUCKET,
            "Endpoint Override URL": S3_ENDPOINT,
            "Access Key": S3_ACCESS_KEY,
            "Secret Key": S3_SECRET_KEY,
            "Region": "us-east-1",
            "Use Path Style Access": "true",
            "Object Key": "debezium/${kafka.topic}/${kafka.partition}/${kafka.offset}.json",
            "Content Type": "application/json"
        }
    )

    # Send to Elasticsearch via HTTP
    putes_id, _ = create_processor(
        root_pg,
        "org.apache.nifi.processors.standard.InvokeHTTP",
        "Elasticsearch Index",
        {"x": 500.0, "y": 350.0},
        {
            "HTTP Method": "POST",
            "Remote URL": f"{ELASTIC_URL}/customers/_doc",
            "Content-Type": "application/json"
        }
    )

    # Connectors
    create_connection(root_pg, consume_id, puts3_id)
    create_connection(root_pg, consume_id, putes_id)

    # Start processors
    for pid in (consume_id, puts3_id, putes_id):
        start_processor(pid)

if __name__ == "__main__":
    main()
