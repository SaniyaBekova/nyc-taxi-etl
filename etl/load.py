from common import get_spark

if __name__ == "__main__":
    # point to your local copy of the Postgres JDBC jar in the Spark image
    POSTGRES_JAR = "/opt/spark/jars/postgresql-42.5.4.jar"

    spark = (
      get_spark("Load")
        .builder
        .config("spark.jars", POSTGRES_JAR)
        .getOrCreate()
    )

    df = spark.read.parquet("/app/etl/data/processed/last6months")

    jdbc_url = "jdbc:postgresql://postgres:5432/rides"
    props = {
        "user": "etl_user",
        "password": "secret",
        "driver": "org.postgresql.Driver"
    }

    # write in parallel (will pick default number of partitions)
    df.write.mode("append").jdbc(jdbc_url, "yellow_trips", properties=props)

    spark.stop()
