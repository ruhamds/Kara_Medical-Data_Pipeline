# 🏥 Kara Medical Data Pipeline – Week 7 Challenge

This project is an end-to-end data pipeline that scrapes Telegram messages from Ethiopian medical business channels, transforms them into a structured PostgreSQL data warehouse using dbt, and prepares them for further enrichment and analysis.

## 📦 Project Overview

- **Source**: Public Telegram Channels (e.g., @lobelia4cosmetics, @tikvahpharma)
- **Objective**: Build a robust, scalable data platform for extracting insights from health-related Telegram content
- **Tools Used**: 
  - `Telethon` for Telegram scraping
  - `Docker + PostgreSQL` for containerized environment and storage
  - `dbt` for data modeling and transformation
  - `Dagster` (coming in Task 5) for orchestration
  - `FastAPI` (Task 4) for building an analytical API
  - `YOLOv8` (Task 3) for image-based enrichment

---

## ✅ Tasks Completed

### ✅ Task 0 – Project Setup & Environment Management

- Initialized Git repository
- Created `requirements.txt`, `Dockerfile`, and `docker-compose.yml`
- Created `.env` for storing secrets (not tracked in Git)
- Used `python-dotenv` to load environment variables
- Project is fully containerized and reproducible

### ✅ Task 1 – Data Scraping and Collection

- Scraped messages and media from Telegram channels using `Telethon`
- Stored raw JSON in a structured directory format:

- Implemented basic logging for scrape status and errors
- Extracted and stored media files (e.g., images)

### ✅ Task 2 – Data Modeling and Transformation (dbt)

- Created a PostgreSQL database and loaded raw JSON into `raw.telegram_messages`
- Initialized a `dbt` project and implemented layered modeling:
- `stg_telegram_messages` (staging)
- `dim_channels`, `dim_dates` (dimension tables)
- `fct_messages` (fact table with >28M messages, including 13M+ with media)
- Added built-in and custom dbt tests (e.g., `not_null`, `unique`, no empty messages)
- Generated project docs and tested pipeline end-to-end

---

## 📂 Project Structure

Kara_Medical_Data_Pipeline/
├── data/
│   └── raw/
│       └── telegram_messages/
│           └── 2025-07-12/
│               ├── lobelia4cosmetics/
│               │   └── messages.json
│               ├── tikvahpharma/
│               │   └── messages.json
│               
│                  
├── Kara_dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_telegram_messages.sql
│   │   └── marts/
│   │       ├── dim_channels.sql
│   │       ├── dim_dates.sql
│   │       └── fct_messages.sql
│   ├── dbt_project.yml
│   └── profiles.yml
├── logs/
│   ├── scrape_telegram.log
│   ├── load_to_postgres.log
│   └── run_dbt.log
├── scripts/
│   ├── scrape_telegram.py
│   ├── load_to_postgres.py
│   └── run_dbt.py
├── .env
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt

## 📝 Next Steps

- **Task 3**: Enrich with YOLOv8 (object detection on images)
- **Task 4**: Build FastAPI analytical endpoints
- **Task 5**: Orchestrate pipeline using Dagster
- **Final Report**: Add diagrams, API screenshots, and reflections