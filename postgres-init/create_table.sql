DROP TABLE IF EXISTS yellow_trips;

CREATE TABLE yellow_trips (
  pickup_ts       TIMESTAMPTZ,
  dropoff_ts      TIMESTAMPTZ,
  passenger_count INTEGER,
  trip_distance   DOUBLE PRECISION,
  fare_amount     DOUBLE PRECISION,
  duration        BIGINT            -- seconds
);
