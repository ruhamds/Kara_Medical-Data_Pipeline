from dagster import job, op, ScheduleDefinition, repository
import subprocess
import os

@op
def scrape_telegram_data():
    subprocess.run(["python", "scripts/scrape_telegram.py"], check=True, cwd=os.getcwd())

@op
def load_raw_to_postgres():
    subprocess.run(["python", "scripts/load_to_postgres.py"], check=True, cwd=os.getcwd())

@op
def run_dbt_transformations():
    subprocess.run(["python", "scripts/run_dbt.py"], check=True, cwd=os.getcwd())

@op
def run_yolo_enrichment():
    subprocess.run(["python", "scripts/enrich_with_yolo.py"], check=True, cwd=os.getcwd())

@job
def medical_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

daily_schedule = ScheduleDefinition(
    job=medical_data_pipeline,
    cron_schedule="0 0 * * *",  # Run daily at midnight
    execution_timezone="Africa/Nairobi"  # EAT timezone
)

@repository
def medical_data_repository():
    return [medical_data_pipeline, daily_schedule]