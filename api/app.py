import os
from typing import List
from datetime import timedelta
import psycopg2
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

DB_USER = os.getenv("POSTGRES_USER",    "etl_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD","secret")
DB_HOST = os.getenv("POSTGRES_HOST",    "postgres")
DB_PORT = os.getenv("POSTGRES_PORT",    "5432")
DB_NAME = os.getenv("POSTGRES_DB",      "rides")

def get_conn():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME
        )
    except Exception as e:
        raise HTTPException(500, detail=f"DB connection error: {e}")

class Trip(BaseModel):
    pickup_ts:      str
    dropoff_ts:     str
    passenger_count: int
    trip_distance:   float
    fare_amount:     float
    duration:        int  # seconds
    vendor_id:           int
    rate_code:          int
    pickup_location_id:  int
    dropoff_location_id: int
    payment_type:        int
    tip_amount:          float
    tolls_amount:        float
    total_amount:        float

app = FastAPI(title="NYC Taxi Trips API")

@app.get("/trips/", response_model=List[Trip])
def list_trips(
    limit:  int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    conn = get_conn()
    cur  = conn.cursor()
    try:
        cur.execute(
            """
            SELECT pickup_ts, dropoff_ts, passenger_count,
                   trip_distance, fare_amount, duration,
                   vendor_id, rate_code, pickup_location_id,
                   dropoff_location_id, payment_type, tip_amount,
                   tolls_amount, total_amount
              FROM yellow_trips
             ORDER BY pickup_ts DESC
             LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    trips: List[Trip] = []
    for row in rows:
        # row[5] is a datetime.timedelta
        d = row[5]
        if isinstance(d, timedelta):
            secs = int(d.total_seconds())
        else:
            secs = int(d)  # in case you ever switch to BIGINT
        trips.append(Trip(
            pickup_ts      = row[0].isoformat(),
            dropoff_ts     = row[1].isoformat(),
            passenger_count= row[2],
            trip_distance  = float(row[3]),
            fare_amount    = float(row[4]),
            duration       = secs,
            vendor_id      = row[6],
            rate_code      = row[7],
            pickup_location_id    = row[8],
            dropoff_location_id   = row[9],
            payment_type     = row[10],
            tip_amount       = float(row[11]),
            tolls_amount     = float(row[12]),
            total_amount     = float(row[13])
        ))

    return trips
