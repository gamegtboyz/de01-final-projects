def collisiontime():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    #import matplotlib.pyplot as plt
    from includes.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT * from collisions"

    # export query to dataframe
    df = pd.read_sql_query(query, engine)

    # answer the question5: Is the time of the day associated with collision frequencies.
    

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#5 task was processed succesfully.")