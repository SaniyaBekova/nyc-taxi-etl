# NYC Taxi ETL Pipeline

This repository contains a full ETL pipeline for NYC Yellow Taxi trip data, implemented using Apache Spark, Docker, and PostgreSQL, with a simple Flask API for data access.

## Data Source

* **Source**: NYC TLC S3 bucket (`https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{YYYY-MM}.csv`) for the last six months of data.

## Transformation Steps

1. **Extraction** (`extract.py`):

   * Download raw CSV files for each month.
   * Convert to Parquet format and store in `/app/etl/data/raw/`.

2. **Transformation** (`transform.py`):

   * Read raw Parquet files with Spark.
   * Filter out trips with `trip_distance <= 0`.
   * Compute `duration` (in seconds) as the difference between dropoff and pickup timestamps.
   * Select and rename fields: `pickup_ts`, `dropoff_ts`, `passenger_count`, `trip_distance`, `fare_amount`, `duration`.
   * Write cleaned data to `/app/etl/data/processed/last6months/` in Parquet.

3. **Loading** (`load.py`):

   * Read processed Parquet data with Spark.
   * Load into PostgreSQL table `yellow_trips` via JDBC in parallel partitions.

## Destination of the Data

* **Database**: PostgreSQL (host: `postgres:5432`, database: `rides`, table: `yellow_trips`).

## Pipeline Automation

* **Containerization**: All components (Spark, PostgreSQL, Flask API) are defined in `docker-compose.yml`.
* **Scheduling**: ETL jobs can be run via `docker compose exec spark spark-submit ...`. For full automation, you can integrate with a scheduler or CI/CD tool.

## REST API

* **Framework**: Flask
* **Endpoint**: `GET /trips?limit=<n>&offset=<m>`
* **Port**: Exposed on `localhost:5001` by default.

## How to Run

1. **Clone the repository**:

   ```bash
   git clone <repo_url>
   cd nyc-taxi-etl
   ```

2. **Start services**:

   ```bash
   docker compose up -d spark postgres api
   ```

3. **Run ETL**:

   ```bash
   docker compose exec spark \
     spark-submit --master local[*] --conf spark.jars.ivy=/tmp/.ivy2 \
     /app/etl/extract.py

   docker compose exec spark \
     spark-submit --master local[*] --conf spark.jars.ivy=/tmp/.ivy2 \
     /app/etl/transform.py

   docker compose exec spark \
     spark-submit --master local[*] --jars /opt/spark/jars/postgresql-42.5.4.jar \
     /app/etl/load.py
   ```

4. **Access the API**:

   ```bash
   curl "http://localhost:5001/trips?limit=10&offset=0"
   ```

## Repository Structure

```
├── spark/                  # Spark Docker image and config
├── api/                    # Flask API code and Dockerfile
├── etl/                    # ETL scripts and data folders
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── docker-compose.yml      # Service definitions (Spark, Postgres, API)
├── create_table.sql        # SQL for creating postgres table
├── .gitignore
└── README.md               # This file
```
