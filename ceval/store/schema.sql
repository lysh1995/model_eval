-- Companion evaluation service -- MySQL schema (the designed production DB).
-- Runs as-is on MySQL 8+. The service also runs on SQLite (stdlib) with the same
-- table definitions via ceval.store.db.ddl("sqlite"); this file is the MySQL dialect.
-- CREATE DATABASE ceval CHARACTER SET utf8mb4; USE ceval;

CREATE TABLE IF NOT EXISTS models (
  id VARCHAR(80) PRIMARY KEY,
  name VARCHAR(255),
  provider VARCHAR(255),
  params JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS prompts (
  id VARCHAR(80) PRIMARY KEY,
  name VARCHAR(255),
  system_prompt LONGTEXT,
  intent VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS variants (
  id VARCHAR(80) PRIMARY KEY,
  model_id VARCHAR(80),
  prompt_id VARCHAR(80),
  anchoring_policy VARCHAR(255),
  label VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS characters (
  id VARCHAR(80) PRIMARY KEY,
  name VARCHAR(255),
  card LONGTEXT,
  language VARCHAR(255),
  prologue LONGTEXT,
  initial_user_input LONGTEXT,
  source VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS dialogues (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  variant_id VARCHAR(80),
  character_id VARCHAR(80),
  run_id VARCHAR(255),
  turns JSON,
  source VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS sessions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  variant_id VARCHAR(80),
  character_id VARCHAR(80),
  arm VARCHAR(255),
  language VARCHAR(255),
  signals JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS evaluators (
  id VARCHAR(80) PRIMARY KEY,
  kind VARCHAR(255),
  model_snapshot VARCHAR(255),
  prompt_hash VARCHAR(255),
  rubric_version VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS grades (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  variant_id VARCHAR(80),
  dimension VARCHAR(255),
  value DOUBLE,
  role VARCHAR(255),
  source VARCHAR(255),
  phase VARCHAR(255),
  language VARCHAR(255),
  evaluator_id VARCHAR(80),
  interval_low DOUBLE,
  interval_high DOUBLE,
  n_effective INT,
  segment VARCHAR(255),
  caveats JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS evidence (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  variant_id VARCHAR(80),
  dimension VARCHAR(255),
  kind VARCHAR(255),
  character_id VARCHAR(80),
  text LONGTEXT,
  score DOUBLE,
  why VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
