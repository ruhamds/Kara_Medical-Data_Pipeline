#  Kara Medical Data Pipeline

A robust, end-to-end data pipeline for extracting, transforming, enriching, and analyzing Telegram messages related to the Ethiopian medical business sector.

---

##  Project Overview

This project collects raw Telegram messages from public medical-related channels, stores them in a PostgreSQL warehouse, enriches the data using YOLOv8 object detection, transforms it with dbt, and serves business insights through a FastAPI analytical API. The pipeline is fully orchestrated with Dagster.

---

## 📂 Directory Structure

Kara_Medical_Data_Pipeline/
│
├── data/ # Raw Telegram messages & media
├── logs/ # Log files
├── scripts/ # Python scripts
│ ├── scrape_telegram.py
│ ├── load_to_postgres.py
│ ├── run_dbt.py
│ ├── enrich_with_yolo.py
│ └── API/ # FastAPI app
│ ├── main.py
│ ├── crud.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
├── kara_dbt/ # dbt project
│ ├── models/
│ │ ├── staging/
│ │ └── marts/
├── dagster_job.py # Dagster job and schedule
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md



---

##  Tasks Breakdown

### ✅ Task 0: Project Setup

* Dockerized environment using `docker-compose`
* PostgreSQL service with persistent volume
* VSCode configured for remote container development

### ✅ Task 1: Data Scraping

* Collected messages from public Telegram medical channels using [Telethon]
* Saved messages in structured JSON format
* Downloaded associated media to a local file system

### ✅ Task 2: Data Modeling with dbt

* Created dbt staging models:
  * `stg_telegram_messages`
  * `stg_detected_objects`
* Built final fact and dimension tables:
  * `fct_messages`, `dim_channels`, `dim_dates`
  * Analytical marts: `top_products`, `top_detected_objects`
* Added dbt tests and documentation

### ✅ Task 3: YOLO Enrichment

* Integrated YOLOv8 for product image detection
* Extracted top-objects per image
* Stored enriched data in PostgreSQL and exposed via dbt models

### ✅ Task 4: Analytical API with FastAPI

* Built API endpoints:
  * `GET /api/reports/top-products?limit=10`
  * `GET /api/channels/{channel_name}/activity`
  * `GET /api/search/messages?query=paracetamol`
* Used SQLAlchemy ORM and Pydantic schemas
* Served insights from dbt models

### ✅ Task 5: Pipeline Orchestration with Dagster

* Converted all scripts into Dagster `ops`
* Defined a complete `medical_data_pipeline` job
* Scheduled the pipeline to run daily at midnight
* Developed and monitored via Dagster UI (`dagster dev`)

---
## 🧩 Data Architecture Flow

graph TD
    A[Telegram Scraper (Telethon)] --> B[Raw JSON + Media files]
    B --> C[PostgreSQL (raw.messages)]
    C --> D[dbt Transformations]
    D --> E[Data Marts (views): top_products, top_detected_objects]
    E --> F[FastAPI Analytical API]
    C --> G[YOLOv8 Image Detection]
    G --> D
    F --> H[API Clients (Swagger, curl)]



##  API Endpoints

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore and test:

| Endpoint | Description |
|----------|-------------|
| `/api/reports/top-products?limit=10` | Most mentioned products |
| `/api/channels/{channel_name}/activity` | Posting trends by channel |
| `/api/search/messages?query=paracetamol` | Keyword search in messages |

---

##  Docker Usage

```
# Start all services
docker-compose up --build

# Stop services
docker-compose down
 Running the Pipeline Manually

python scripts/scrape_telegram.py
python scripts/load_to_postgres.py
python scripts/run_dbt.py
python scripts/enrich_with_yolo.py
 Schedule via Dagster

dagster dev
Open Dagster UI at: http://localhost:3000

 Future Improvements
Deploy API with HTTPS and token-based auth

Move media to cloud storage (e.g., AWS S3 or Azure Blob)

Add alerts for pipeline failures

Auto-refresh dashboard using Superset or Streamlit

