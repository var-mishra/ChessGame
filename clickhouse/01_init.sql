-- Create analytics database and raw table populated via Kafka engine + MV
CREATE DATABASE IF NOT EXISTS cdc;

-- Destination analytical table
CREATE TABLE IF NOT EXISTS cdc.debezium_raw (
  event_time DateTime DEFAULT now(),
  op String,
  id Int32,
  first_name String,
  last_name String,
  email String
) ENGINE = MergeTree()
ORDER BY (id, event_time);

-- Kafka raw topic reader (each message as a single line String)
CREATE TABLE IF NOT EXISTS cdc.kafka_customers (
  raw String
) ENGINE = Kafka()
SETTINGS
  kafka_broker_list = 'kafka:9092',
  kafka_topic_list = 'dbserver1.inventory.customers',
  kafka_group_name = 'ch_cdc_consumer',
  kafka_format = 'LineAsString',
  kafka_num_consumers = 1;

-- Materialized view to parse Debezium envelope and insert into destination table
CREATE MATERIALIZED VIEW IF NOT EXISTS cdc.mv_customers TO cdc.debezium_raw AS
SELECT
  now() AS event_time,
  JSONExtractString(raw, 'op') AS op,
  toInt32OrNull(JSONExtractString(JSONExtractRaw(raw, 'after'), 'id')) AS id,
  JSONExtractString(JSONExtractRaw(raw, 'after'), 'first_name') AS first_name,
  JSONExtractString(JSONExtractRaw(raw, 'after'), 'last_name') AS last_name,
  JSONExtractString(JSONExtractRaw(raw, 'after'), 'email') AS email
FROM cdc.kafka_customers;
