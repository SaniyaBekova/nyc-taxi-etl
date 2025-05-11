import datetime
from common import get_spark

def last_n_months(n):
    today = datetime.date.today().replace(day=1)
    for i in range(n):
        m = today - datetime.timedelta(days=1)
        yield m.year, m.month
        today = m.replace(day=1)

if __name__ == "__main__":
    spark = get_spark("Extract")
    raw_base = "/app/etl/data/raw"

    for year, month in last_n_months(6):
        ym = f"{year:04d}-{month:02d}"
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{ym}.parquet"
        print(f"→ Reading {url}")
        df = spark.read.parquet(url)
        out = f"{raw_base}/{ym}.parquet"
        print(f"→ Writing raw month to {out}")
        df.write.mode("overwrite").parquet(out)

    spark.stop()
