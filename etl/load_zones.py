from common import get_spark

if __name__ == "__main__":
    spark = get_spark("LoadZones")

    # читаем CSV
    df = (
        spark.read
             .option("header", True)
             .option("inferSchema", True)
             .csv("/app/etl/data/reference/taxi_zone_lookup.csv")
    )

    # приводим названия колонок к lower_snake_case
    df = (
        df.withColumnRenamed("LocationID", "location_id")
          .withColumnRenamed("Borough",     "borough")
          .withColumnRenamed("Zone",        "zone")
          .withColumnRenamed("service_zone","service_zone")
    )

    # JDBC-параметры
    jdbc_url = "jdbc:postgresql://postgres:5432/rides"
    props = {"user":"etl_user", "password":"secret", "driver":"org.postgresql.Driver"}

    # записываем в Postgres
    df.write \
      .mode("overwrite") \
      .jdbc(jdbc_url, "taxi_zones", properties=props)

    spark.stop()
