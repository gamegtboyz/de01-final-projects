def dbload():
    # download the relevant library
    import pandas as pd
    from sqlalchemy import create_engine
    from includes.db_config import connection_string

    # download the file onto the dataframe
    df = pd.read_csv('includes/outputs/nyc-collisions.csv')

    # create database connection
    engine = create_engine(connection_string)

    # write dataframe to sql
    table_name = 'collisions'

    try:
        df.to_sql(table_name,engine,if_exists='replace',index=False)
        print(f"DataFrame was written to '{table_name}' table succesfully.")
    except Exception as e:
        print("Error: ", e)

    # close database connection
    engine.dispose()