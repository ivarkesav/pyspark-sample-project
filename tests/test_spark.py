import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, length, lower, regexp_replace, split


@pytest.fixture(scope="module")
def spark():
    session = (
        SparkSession.builder.appName("TestPySparkSample")
        .master("local[1]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    yield session
    session.stop()


DATA = [
    (1, "Spark makes large-scale data processing simpler"),
    (2, "PySpark lets you use Python for distributed jobs"),
    (3, "Spark submit can run jobs locally with Docker"),
]


def test_dataframe_creation(spark):
    df = spark.createDataFrame(DATA, ["id", "text"])

    assert df.count() == 3
    assert df.columns == ["id", "text"]
    assert df.schema["id"].dataType.simpleString() == "bigint"
    assert df.schema["text"].dataType.simpleString() == "string"


def test_word_count(spark):
    df = spark.createDataFrame(DATA, ["id", "text"])

    words = df.select(
        explode(
            split(lower(regexp_replace(col("text"), r"[^a-zA-Z0-9\s]", "")), r"\s+")
        ).alias("word")
    ).filter(length(col("word")) > 0)

    counts = words.groupBy("word").count().orderBy(col("count").desc(), col("word"))

    rows = {row["word"]: row["count"] for row in counts.collect()}

    assert rows["spark"] == 2
    assert rows["jobs"] == 2
    assert rows["pyspark"] == 1
    assert rows["data"] == 1
    assert rows["docker"] == 1
    # hyphen stripped so "large-scale" becomes "largescale"
    assert "largescale" in rows
    assert "large-scale" not in rows
