DROP TABLE IF EXISTS yellow_trips;

CREATE TABLE yellow_trips (
  pickup_ts           TIMESTAMPTZ,
  dropoff_ts          TIMESTAMPTZ,
  passenger_count     INTEGER,
  trip_distance       DOUBLE PRECISION,
  fare_amount         DOUBLE PRECISION,
  duration            BIGINT,            -- seconds
  vendor_id           INTEGER,
  rate_code           INTEGER,
  pickup_location_id  INTEGER,
  dropoff_location_id INTEGER,
  payment_type        INTEGER,
  tip_amount          DOUBLE PRECISION,
  tolls_amount        DOUBLE PRECISION,
  total_amount        DOUBLE PRECISION
);
