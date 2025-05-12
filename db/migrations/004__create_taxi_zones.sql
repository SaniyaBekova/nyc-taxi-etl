-- 004__create_taxi_zones.sql

CREATE TABLE IF NOT EXISTS taxi_zones (
  location_id   SMALLINT PRIMARY KEY,
  borough       TEXT        NOT NULL,
  zone          TEXT        NOT NULL,
  service_zone  TEXT        NOT NULL
);
