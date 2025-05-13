# NYC Taxi ETL Pipeline

This repository contains an automated ETL (Extract, Transform, Load) pipeline for processing NYC Yellow Taxi trip data.

## Data Source

* **NYC Taxi & Limousine Commission (TLC)** dataset:

  * URL format: `https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{YYYY-MM}.csv`
  * The pipeline fetches and processes data from the most recent six months.

## Transformation Steps

### Extraction

* Raw CSV data files are downloaded and converted to Parquet format.
* Stored locally within the pipeline environment (`/app/etl/data/raw/`).

### Transformation

* Data cleaning with Apache Spark:

  * Filters out invalid records (e.g., trips with `trip_distance <= 0`).
  * Computes additional fields such as trip duration (`duration`) in seconds.
  * Fields selected and standardized include timestamps, passenger counts, distances, fare details, payment types, and location identifiers.
* Transformed data is stored in Parquet format (`/app/etl/data/processed/`).

### Loading

* Cleaned and transformed data is loaded into PostgreSQL using Spark's JDBC interface.
* The destination database and tables are optimized with proper indexing and foreign key constraints.

## Destination of Data

* **PostgreSQL Database**:

  * Host: `postgres:5432`
  * Database: `rides`
  * Table: `yellow_trips`
  * Additional reference tables: `rate_codes`, `payment_types`

## Automation

* Pipeline components (Spark, PostgreSQL, Flask API) are containerized using Docker Compose.

### Running the Pipeline

```bash
docker compose up -d

# Run ETL tasks:
docker compose exec spark spark-submit /app/etl/extract.py
docker compose exec spark spark-submit /app/etl/transform.py
docker compose exec spark spark-submit --jars /opt/spark/jars/postgresql-42.5.4.jar /app/etl/load.py
```


## Accessing Data

* Flask-based REST API:

  ```bash
  curl "http://localhost:5001/trips?limit=10&offset=0"
  ```


