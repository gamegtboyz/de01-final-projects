# import text and datetime library, we will use it for scheduling activities.
import textwrap
from datetime import datetime, timedelta
import subprocess

# import DAG
from airflow.models.dag import DAG

# import operators package
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# instantiate a DAG
with DAG (
    dag_id = 'de01-final-project-dag',       # defile dag-id
        # set up the default arguments. Default arguments means we predefine the default values then apply it to all operators defined in this dag
    default_args = {
        'depends_on_past': False,
        'email': ['test@airflow.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'start_date': datetime(2024, 12, 28),
        'schedule_interval': '0 11 * * *',   # run daily at noon (CET)
        'retries': 10,
        'retry_delay': timedelta(minutes=1)
    }
) as dag:

    # set the tasks list
    # define the function to execute a python scripts
    # # t1 is an execution of download and cleanup file
    def load_and_clean(**kwargs):
        result = subprocess.run(['python','nyc-collisions-download-cleanup.py'],capture_output=True,text=True)
        print(result.stdout)    # this line is to print script output
        if result.returncode != 0:
            raise Exception(f'Script failed with error: {result.stderr}')
    
    t1 = PythonOperator(
        task_id = 'load-and-clean',
        python_callable = load_and_clean,
        dag = dag
    )

    # set task dependencies
    t1