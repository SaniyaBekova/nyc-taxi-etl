ARG SPARK_VERSION=3.5.5
FROM openjdk:17-jdk-slim

# install Python & curl
RUN apt-get update \
 && apt-get install -y python3 python3-pip curl tar procps \
 && rm -rf /var/lib/apt/lists/*

# download Spark
ARG HADOOP_PROFILE=hadoop3
RUN curl -fsSL \
    "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE}.tgz" \
  | tar -xz -C /opt \
 && mv /opt/spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE} /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# grab Postgres JDBC
ARG PG_VER=42.5.4
RUN curl -fsSL \
    "https://repo1.maven.org/maven2/org/postgresql/postgresql/${PG_VER}/postgresql-${PG_VER}.jar" \
  -o $SPARK_HOME/jars/postgresql-${PG_VER}.jar

# copy your ETL code
COPY etl /app/etl
WORKDIR /app/etl

# install python deps if any (e.g. dateutil)
RUN pip3 install python-dateutil

CMD ["tail", "-f", "/dev/null"]
