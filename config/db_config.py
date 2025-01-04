db_config = {
    'user': 'airflow',
    'password': 'airflow',
    'host': 'postgres',
    'port': 5432,
    'database': 'airflow'
    }

connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"