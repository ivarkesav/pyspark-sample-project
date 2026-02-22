# PySpark Sample Project (Docker + spark-submit)

This project runs a simple PySpark word-count job using a local Spark master/worker setup in Docker.

## Project structure

- `app/job.py`: sample PySpark job
- `Dockerfile`: image used for submitting jobs
- `docker-compose.yml`: Spark cluster + submit service
- `scripts/submit.sh`: helper script that runs `spark-submit`

## Prerequisites

- Docker Desktop (or Docker Engine with Compose plugin)

## Run the sample

From `/Users/alpha/CODEX/pyspark-sample-project`:

```bash
docker compose build

docker compose up -d spark-master spark-worker

# Submit the sample job
docker compose run --rm spark-submit
```

You should see word-count output in the command logs.

## Spark UI

- Master UI: [http://localhost:8080](http://localhost:8080)
- Worker UI: [http://localhost:8081](http://localhost:8081)

## Stop and clean up

```bash
docker compose down
```

## Image tag note

Docker Hub no longer resolves `bitnami/spark` tags used earlier. This project now defaults to `apache/spark:latest`.
If you want to pin a specific valid tag, set `SPARK_IMAGE`:

```bash
SPARK_IMAGE=apache/spark:<valid-tag> docker compose build
SPARK_IMAGE=apache/spark:<valid-tag> docker compose up -d spark-master spark-worker
SPARK_IMAGE=apache/spark:<valid-tag> docker compose run --rm spark-submit
```
