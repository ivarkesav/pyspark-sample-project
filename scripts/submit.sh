#!/usr/bin/env bash
set -euo pipefail

SPARK_HOME=${SPARK_HOME:-/opt/spark}
MASTER_URL=${SPARK_MASTER_URL:-spark://spark-master:7077}

"${SPARK_HOME}/bin/spark-submit" \
  --master "${MASTER_URL}" \
  /opt/spark-apps/job.py
