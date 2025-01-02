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
from includes.q1_collisioncause import collisioncause
from includes.q2_collisionvehicle import collisionvehicle
from includes.q3_collisionmap import collisionmap
from includes.q4_casualityrate import casualityrate
from includes.q5_collisiontime import collisiontime

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
    start_date = datetime(2025, 1, 1)
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

    q1 = PythonOperator(
        task_id = 'q1-collisioncause',
        python_callable = collisioncause,
        dag = dag
    )

    q2 = PythonOperator(
        task_id = 'q2-collisionvehicle',
        python_callable = collisionvehicle,
        dag = dag
    )

    q3 = PythonOperator(
        task_id = 'q3-collisionmap',
        python_callable = collisionmap,
        dag = dag
    )

    q4 = PythonOperator(
        task_id = 'q4-casualityrate',
        python_callable = casualityrate,
        dag = dag
    )

    q5 = PythonOperator(
        task_id = 'q5-collisiontime',
        python_callable = collisiontime,
        dag = dag
    )

    # set task dependencies
    t1 >> t2 >> q1 >> q2 >> q3 >> q4 >> q5