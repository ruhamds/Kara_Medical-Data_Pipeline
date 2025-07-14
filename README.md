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

Kara_Medical_Data_Pipeline/
│
├── data/                               # Raw and sample Telegram message data
│   └── raw/
│       └── telegram_messages/
│           └── 2025-07-12/
│               ├── lobelia4cosmetics/     # Sample scraped messages from Lobelia
│               │   └── messages.json
│               ├── tikvahpharma/          # Sample scraped messages from Tikvah Pharma
│               │   └── messages.json
│
├── kara_dbt/                           # dbt project for data modeling and transformation
│   ├── dbt_project.yml                 # Main dbt project config
│   ├── profiles.yml                    # dbt connection config
│   └── models/
│       ├── staging/                    # Staging models (cleaning and structuring)
│       │   └── stg_telegram_messages.sql
│       └── marts/                      # Final star schema models
│           ├── dim_channels.sql
│           ├── dim_dates.sql
│           └── fct_messages.sql
│
├├── logs/                               # Log files for scraping, loading, and dbt runs
│   ├── scrape_telegram.log             # (Large, not tracked; sample available on demand)
│   ├── dbt.log                         # (Large, not tracked)
│   ├── run_dbt.log                     # (Small sample log)
│   └── load_to_postgres.log            # (Small sample log)

│
├── scripts/                            # Core pipeline scripts
│   ├── scrape_telegram.py              # Scrapes Telegram channels
│   ├── load_to_postgres.py             # Loads raw JSON into PostgreSQL
│   └── run_dbt.py                      # Runs dbt transformation
│
├── .env.example                        # Example environment variables
├── .dockerignore
├── .gitignore
├── docker-compose.yml                 # Orchestrates services (PostgreSQL + app)
├── Dockerfile                         # Python environment container
├── requirements.txt                   # Python dependencies
└── README.md                          # Project overview and instructions



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
