CREATE TABLE monitoring_recordings(
    id uuid PRIMARY KEY,
    name string unique NOT NULL,
    is_send bool NOT NULL DEFAULT FALSE
);