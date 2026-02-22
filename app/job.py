from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, lower, regexp_replace, split, explode


def main() -> None:
    spark = (
        SparkSession.builder.appName("LocalPySparkSample")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    data = [
        (1, "Spark makes large-scale data processing simpler"),
        (2, "PySpark lets you use Python for distributed jobs"),
        (3, "Spark submit can run jobs locally with Docker"),
    ]

    df = spark.createDataFrame(data, ["id", "text"])

    words = (
        df.select(explode(split(lower(regexp_replace(col("text"), r"[^a-zA-Z0-9\\s]", "")), r"\\s+")).alias("word"))
        .filter(length(col("word")) > 0)
    )

    counts = words.groupBy("word").count().orderBy(col("count").desc(), col("word"))

    print("Word count results:")
    counts.show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
