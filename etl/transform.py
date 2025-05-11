from common import get_spark
from pyspark.sql.functions import col

if __name__ == "__main__":
    spark = get_spark("Transform")

    raw_base = "/app/etl/data/raw"
    processed_base = "/app/etl/data/processed"
    # read *all* the last-six-months
    df = spark.read.parquet(f"{raw_base}/*.parquet")

    # filter out zero‐distance trips
    df2 = df.filter(col("trip_distance") > 0)

    # compute duration in seconds
    df3 = df2.withColumn(
        "duration",
        (col("tpep_dropoff_datetime").cast("timestamp")
         .cast("long")
        - col("tpep_pickup_datetime").cast("timestamp")
         .cast("long"))
    )

    # select and rename
    out = df3.select(
      col("tpep_pickup_datetime").alias("pickup_ts"),
      col("tpep_dropoff_datetime").alias("dropoff_ts"),
      col("passenger_count"),
      col("trip_distance"),
      col("fare_amount"),
      col("duration")
    )

    # write one Parquet for all six months
    out.write.mode("overwrite").parquet(f"{processed_base}/last6months")

    spark.stop()
