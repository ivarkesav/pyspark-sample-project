ARG SPARK_IMAGE=apache/spark:latest
FROM ${SPARK_IMAGE}

USER root
COPY app /opt/spark-apps
COPY scripts/submit.sh /opt/spark-scripts/submit.sh
RUN chmod +x /opt/spark-scripts/submit.sh

WORKDIR /opt/spark
CMD ["tail", "-f", "/dev/null"]
