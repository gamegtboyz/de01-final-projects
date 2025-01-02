def casualityrate():
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

    # answer the question4: What is the vehicle type with most casuality rate
    

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#4 task was processed succesfully.")