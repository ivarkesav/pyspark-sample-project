"""PySpark word count job with UTC timestamp display."""

import os
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
os.environ.setdefault("SPARK_CONF_DIR", str(Path(__file__).resolve().parent / "spark-conf"))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, lower, regexp_replace, split, explode


def display_utc_datetime() -> None:
    now = datetime.now(timezone.utc)
    time_str = f"Current UTC date/time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}"
    separator = "*" * len(time_str)
    print(separator)
    print(time_str)
    print(separator)


def main() -> None:
    """Run the PySpark word count job and display results."""
    spark = (
        SparkSession.builder.appName("LocalPySparkSample")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.driver.host", "localhost")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    data = [
        (1, "Spark makes large-scale data processing simpler"),
        (2, "PySpark lets you use Python for distributed jobs"),
        (3, "Spark submit can run jobs locally with Docker"),
    ]

    df = spark.createDataFrame(data, ["id", "text"])

    words = (
        df.select(explode(split(lower(regexp_replace(col("text"), r"[^a-zA-Z0-9\s]", "")), r"\s+")).alias("word"))
        .filter(length(col("word")) > 0)
    )

    counts = words.groupBy("word").count().orderBy(col("count").desc(), col("word"))

    print("Word count results:")
    counts.show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    display_utc_datetime()
    main()
