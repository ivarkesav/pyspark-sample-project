# PySpark Sample Project (Docker + spark-submit)

A containerized PySpark word-count application that runs on a local Spark cluster using Docker Compose. The project demonstrates how to set up a Spark master/worker topology, submit Python jobs via `spark-submit`, and test PySpark logic with pytest.

## Architecture

```mermaid
graph LR
    subgraph Docker Network
        M[Spark Master<br/>:7077 / :8080] -->|registers| W[Spark Worker<br/>:8081]
        S[spark-submit<br/>container] -->|submits job| M
        W -->|executes tasks| S
    end

    subgraph Host
        A[app/job.py] -->|mounted volume| S
        SC[scripts/submit.sh] -->|mounted volume| S
        B[Browser] -->|Master UI :8080| M
        B -->|Worker UI :8081| W
    end
```

## Project Structure

```
pyspark-sample-project/
├── app/
│   └── job.py                 # PySpark word-count job
├── scripts/
│   └── submit.sh              # spark-submit wrapper
├── tests/
│   ├── conftest.py            # Spark session fixtures & env setup
│   ├── spark-conf/
│   │   └── log4j2.properties  # Suppresses noisy Spark logs in tests
│   ├── test_spark.py          # DataFrame creation & word-count tests
│   └── test_utc.py            # UTC datetime display test
├── docker-compose.yml         # Master, Worker, Submit services
├── Dockerfile                 # Extends apache/spark image
├── pyproject.toml             # Project metadata & dependencies
├── uv.lock                    # Locked dependency versions
└── .env                       # Default SPARK_IMAGE variable
```

## Job Execution Flow

```mermaid
flowchart TD
    A[Start job.py] --> B[display_utc_datetime]
    B --> C[Print current UTC time<br/>with separator lines]
    C --> D[Create SparkSession<br/>app: LocalPySparkSample]
    D --> E[Build DataFrame<br/>3 rows of sample text]
    E --> F[Transform Pipeline]

    subgraph F[Transform Pipeline]
        direction TB
        F1[lowercase all text] --> F2[strip special characters]
        F2 --> F3[split into words]
        F3 --> F4[explode into rows]
        F4 --> F5[filter empty strings]
    end

    F --> G[Group by word & count]
    G --> H[Order by count desc,<br/>word asc]
    H --> I[Display results table]
    I --> J[Stop SparkSession]
```

## Data Pipeline

```mermaid
flowchart LR
    subgraph Input
        R1["(1, 'Spark makes large-scale<br/>data processing simpler')"]
        R2["(2, 'PySpark lets you use<br/>Python for distributed jobs')"]
        R3["(3, 'Spark submit can run<br/>jobs locally with Docker')"]
    end

    Input -->|createDataFrame| DF[DataFrame<br/>id · text]
    DF -->|lower + regexp_replace<br/>split + explode + filter| Words[Words DataFrame<br/>word]
    Words -->|groupBy · count<br/>orderBy| Counts[Word Counts<br/>word · count]
    Counts -->|show| Output["spark: 2<br/>jobs: 2<br/>can: 1<br/>data: 1<br/>..."]
```

## Docker Services

```mermaid
graph TB
    subgraph docker-compose.yml
        Master["spark-master<br/>───────────<br/>Ports: 7077, 8080<br/>Image: apache/spark:latest"]
        Worker["spark-worker<br/>───────────<br/>Port: 8081<br/>1 core · 1 GB RAM"]
        Submit["spark-submit<br/>───────────<br/>Built from Dockerfile<br/>Runs submit.sh"]
    end

    Master --- |"spark://spark-master:7077"| Worker
    Submit --> |"spark-submit --master<br/>spark://spark-master:7077<br/>/opt/spark-apps/job.py"| Master

    Master -.->|depends_on| Worker
    Submit -.->|depends_on| Master
    Submit -.->|depends_on| Worker
```

## Prerequisites

- Docker Desktop (or Docker Engine with the Compose plugin)
- Python 3.12+ and [uv](https://docs.astral.sh/uv/) (for local development and testing only)

## Run the Sample

```bash
# Build the spark-submit image
docker compose build

# Start the Spark cluster
docker compose up -d spark-master spark-worker

# Submit the PySpark job
docker compose run --rm spark-submit
```

Expected output:

```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Current UTC date/time: 2026-02-27 12:30:45 UTC
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Word count results:
+----------+-----+
|word      |count|
+----------+-----+
|jobs      |2    |
|spark     |2    |
|can       |1    |
|data      |1    |
|distributed|1   |
|docker    |1    |
|for       |1    |
|largescale|1    |
|lets      |1    |
|locally   |1    |
|...       |...  |
+----------+-----+
```

## Testing

Tests run locally using a single-node Spark session (no Docker required):

```bash
# Install dev dependencies
uv sync

# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_utc.py -v
```

```mermaid
graph LR
    subgraph Test Suite
        T1[test_dataframe_creation<br/>Validates schema & row count]
        T2[test_word_count<br/>Verifies word frequencies<br/>& special-char stripping]
        T3[test_display_utc_datetime<br/>Checks formatted output<br/>with separator lines]
    end

    T1 & T2 -->|uses| SF[SparkSession fixture<br/>local mode]
    T3 -->|uses| Mock[Mocked datetime]
```

## Spark UI

While the cluster is running:

| UI | URL |
|---|---|
| Master | [http://localhost:8080](http://localhost:8080) |
| Worker | [http://localhost:8081](http://localhost:8081) |

## Stop and Clean Up

```bash
docker compose down
```

## Configuration

### Spark image

The default image is `apache/spark:latest` (set in `.env`). Override it with the `SPARK_IMAGE` variable:

```bash
SPARK_IMAGE=apache/spark:<tag> docker compose build
SPARK_IMAGE=apache/spark:<tag> docker compose up -d spark-master spark-worker
SPARK_IMAGE=apache/spark:<tag> docker compose run --rm spark-submit
```

### Dependencies

Managed with [uv](https://docs.astral.sh/uv/) via `pyproject.toml`:

| Package | Role |
|---|---|
| `pyspark >=4.1.1` | Spark Python API |
| `pytest >=9.0.2` | Test framework (dev) |
