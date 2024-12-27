# import text and datetime library, we will use it for scheduling activities.
import textwrap
from datetime import datetime, timedelta

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
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    }
) as dag:

    # set the tasks list
    t1 = BashOperator(
        task_id = 'test',
        bash_command = 'echo "hello world"',
        dag = dag
    )

    # set task dependencies
    t1