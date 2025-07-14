# 🏥 Kara Medical Data Pipeline – Week 7 Challenge

This project delivers an end-to-end data pipeline for analyzing Ethiopian medical business activity using public Telegram channels.

## 📦 Project Overview

- **Source**: Public Telegram Channels (e.g., @lobelia4cosmetics, @tikvahpharma)
- **Objective**: Scrape messages and media from Telegram, store as raw JSON, load into PostgreSQL, and transform using dbt
- **Tools**:
  - Telethon (scraping)
  - PostgreSQL + Docker
  - dbt (data transformation)
  - Dagster (orchestration)
  - YOLOv8 (image enrichment – Task 3)
  - FastAPI (analytical API – Task 4)

---

## ✅ Tasks Completed

### ✅ Task 0 – Project Setup

- Git repository initialized
- Dockerized Python + PostgreSQL environment
- `.env` secrets management and `.gitignore` used
- `requirements.txt` for dependencies

### ✅ Task 1 – Telegram Scraping and Data Collection

- Scraped messages from:
  - `@lobelia4cosmetics`
  - `@tikvahpharma`
- Media downloaded (images)
- Data stored in structured folders like:
- ✅ **Sample JSON files** included:
- [`tikvah_sample.json`](data/raw/telegram_messages/2025-07-12/tikvahpharma/messages.json)
- [`lobelia_sample.json`](data/raw/telegram_messages/2025-07-12/lobelia4cosmetics/messages.json)

### ✅ Task 2 – Data Modeling with dbt

- Loaded raw JSON into PostgreSQL (`raw.telegram_messages`)
- Created dbt models:
- `stg_telegram_messages` (staging)
- `dim_channels`, `dim_dates` (dimensions)
- `fct_messages` (fact table with 28M+ messages, 13M+ media)
- dbt tests: `unique`, `not_null`, and custom checks
- dbt docs generated

---

## 📂 Project Structure

``` Kara_Medical_Data_Pipeline/ ├── data/ │ └── raw/ │ └── telegram_messages/ │ └── 2025-07-12/ │ ├── lobelia4cosmetics/ │ │ └── messages.json │ ├── tikvahpharma/ │ │ └── messages.json │ ├── kara_dbt/ │ ├── models/ │ │ ├── staging/ │ │ │ └── stg_telegram_messages.sql │ │ └── marts/ │ │ ├── dim_channels.sql │ │ ├── dim_dates.sql │ │ └── fct_messages.sql │ ├── dbt_project.yml │ └── profiles.yml │ ├── logs/ │ ├── scrape_telegram.log │ ├── load_to_postgres.log │ └── run_dbt.log │ ├── scripts/ │ ├── scrape_telegram.py │ ├── load_to_postgres.py │ └── run_dbt.py │ ├── .env ├── .dockerignore ├── .gitignore ├── docker-compose.yml ├── README.md └── requirements.txt ```

---

## 🚀 How to Run This Project


# 1. Clone repo & configure secrets
cp .env.example .env

# 2. Start containers
docker-compose up -d

# 3. Run the Telegram scraper
python scripts/telegram_scraper.py

# 4. Load scraped data into Postgres
python scripts/load_to_postgres.py

# 5. Run dbt transformations
python scripts/run_dbt.py
