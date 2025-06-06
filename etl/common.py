from pyspark.sql import SparkSession

def get_spark(app_name: str):
    return (
        SparkSession.builder
          .appName(app_name)
          .config("spark.sql.session.timeZone", "UTC")
          .getOrCreate()
    )
