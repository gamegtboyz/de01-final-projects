def dbload():
    # download the relevant library
    import pandas as pd
    from sqlalchemy import create_engine

    # download the file onto the dataframe
    df = pd.read_csv('includes/nyc-collisions.csv')

    # configure database connection (we will use it to build up connection string)
    db_config = {
        'user': 'airflow',
        'password': 'airflow',
        'host': 'localhost',
        'port': 5432,
        'database': 'airflow'
    }

    # create database connection string
    connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

    # create engine
    engine = create_engine(connection_string)

    # write dataframe to sql
    table_name = 'collisions'

    try:
        df.to_sql(table_name,engine,if_exists='replace',index=False)
        print(f"DataFrame was written to '{table_name}' table succesfully.")
    except Exception as e:
        print("Error: ", e)