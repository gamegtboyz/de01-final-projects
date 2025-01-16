def collisioncause():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    import matplotlib.pyplot as plt
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT \
        contributing_factor_vehicle_1,\
        contributing_factor_vehicle_2,\
        contributing_factor_vehicle_3,\
        contributing_factor_vehicle_4,\
        contributing_factor_vehicle_5 \
        from collisions"

    # export query to dataframe
    collision_data = pd.read_sql_query(query, engine)

    # answer the question1: What are the 10 most common cause (a.k.a contributing factor) for vehicle collision.
    contributing_factors = collision_data[['contributing_factor_vehicle_1', 'contributing_factor_vehicle_2', 'contributing_factor_vehicle_3', 'contributing_factor_vehicle_4', 'contributing_factor_vehicle_5']].stack().value_counts().drop(labels='Unspecified').head(10)
    plt.figure(figsize=(10, 6))
    contributing_factors.sort_values().plot(kind='barh', color='skyblue', title="Top Contributing Factors for Vehicle Collisions")
    plt.xlabel("Number of Collisions")
    plt.ylabel("Contributing Factors")
    plt.tight_layout()
    plt.savefig("includes/outputs/figures/1_top_contributing_factors.svg", format="svg")

    # create the new qury to extract the table accordingly
    query_t = "SELECT contributing_factor, COUNT(*) AS factor_count\
                FROM (\
                    SELECT contributing_factor_vehicle_1 AS contributing_factor FROM collisions\
                    UNION ALL\
                    SELECT contributing_factor_vehicle_2 FROM collisions\
                    UNION ALL\
                    SELECT contributing_factor_vehicle_3 FROM collisions\
                    UNION ALL\
                    SELECT contributing_factor_vehicle_4 FROM collisions\
                    UNION ALL\
                    SELECT contributing_factor_vehicle_5 FROM collisions\
                ) contributing_factors\
                WHERE contributing_factor <> 'Unspecified'\
                GROUP BY contributing_factor\
                ORDER BY factor_count DESC\
                LIMIT 10;\
                "
    collision_data_t = pd.read_sql_query(query_t, engine)

    collision_data_t.to_csv('includes/outputs/tables/table1.csv')

    # close database connection
    engine.dispose()

    # inform the processing results onto log file
    print("Question#1 task was processed succesfully.")