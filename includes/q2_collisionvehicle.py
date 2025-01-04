def collisionvehicle():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    #import matplotlib.pyplot as plt
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT * from collisions"

    # export query to dataframe
    df = pd.read_sql_query(query, engine)

    # answer the question2: Which 10 type of vehicle are most common in collisions.
    

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#2 task was processed succesfully.")