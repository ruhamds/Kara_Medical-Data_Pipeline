import os
import subprocess
import logging
from pathlib import Path

# Set up logging
Path('logs').mkdir(exist_ok=True)
logging.basicConfig(
    filename='logs/run_dbt.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_dbt():
    try:
        # Define path to dbt project folder
        project_path = Path(__file__).resolve().parent.parent / 'kara_dbt'
        if not project_path.exists():
            raise FileNotFoundError(f"DBT project path does not exist: {project_path}")
        
        # Change directory to dbt project
        os.chdir(project_path)
        logger.info(f"Changed working directory to {project_path}")

        # Run dbt with live output
        process = subprocess.Popen(['dbt', 'run'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)

        for line in process.stdout:
            print(line, end='')
            logger.info(line.strip())

        process.wait()
        if process.returncode != 0:
            raise Exception("❌ dbt run failed")
        print("\n✅ dbt run completed successfully")

    except Exception as e:
        logger.error(f"Error running dbt: {str(e)}")
        print(f"❌ Error running dbt: {e}")
        raise
    finally:
        # Return to original directory
        os.chdir(Path(__file__).resolve().parent.parent)
        logger.info("Returned to original directory")

if __name__ == '__main__':
    run_dbt()