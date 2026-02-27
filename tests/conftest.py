import os
from pathlib import Path

_CONF_DIR = str(Path(__file__).parent / "spark-conf")

os.environ["SPARK_CONF_DIR"] = _CONF_DIR
os.environ["PYSPARK_SUBMIT_ARGS"] = "pyspark-shell"
