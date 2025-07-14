CREATE TABLE monitoring_recordings(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) unique NOT NULL,
    is_sent BOOLEAN NOT NULL DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    human_analysis_status VARCHAR(255) NOT NULL DEFAULT 'NONE'
);