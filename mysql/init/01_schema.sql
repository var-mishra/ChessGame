-- Create application schema and sample data
CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;

CREATE TABLE IF NOT EXISTS customers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (first_name, last_name, email) VALUES
('Alice', 'Anderson', 'alice@example.com'),
('Bob', 'Brown', 'bob@example.com'),
('Carol', 'Clark', 'carol@example.com')
ON DUPLICATE KEY UPDATE email=VALUES(email);
