# import text and datetime library, we will use it for scheduling activities.
import textwrap
from datetime import datetime, timedelta

# import DAG
from airflow.models.dag import DAG

# import operators package
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# import the python callable function
from includes.nyc_collisions_download_cleanup import load_and_clean
from includes.nyc_collisions_dbloader import dbload

# instantiate a DAG
with DAG (
    dag_id = 'de01-final-project-dag',       # define dag-id
        # set up the default arguments. 
        # Default arguments means we predefine the default values then apply it to all operators defined in this dag.
    default_args = {
        'depends_on_past': False,
        'email': ['test@airflow.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta(minutes=10)
    },
    schedule = timedelta(days=1),
    start_date = datetime(2024, 12, 28)
) as dag:

    # set the tasks list
    
    t1 = PythonOperator(
        task_id = 'load-and-clean',
        python_callable = load_and_clean,
        dag = dag
    )

    t2 = PythonOperator(
        task_id = 'load-to-db',
        python_callable = dbload,
        dag = dag
    )

    # set task dependencies
    t1 >> t2