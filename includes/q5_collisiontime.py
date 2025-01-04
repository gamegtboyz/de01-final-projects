def collisiontime():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    import matplotlib.pyplot as plt
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT * from collisions"

    # export query to dataframe
    collision_data = pd.read_sql_query(query, engine)

    # answer the question5: Is the time of the day associated with collision frequencies.
    collision_data['crash_hour'] = pd.to_datetime(collision_data['crash_time'], format='%H:%M', errors='coerce').dt.hour
    collision_data['time_of_day'] = collision_data['crash_hour'].apply(
        lambda x: 'Daytime' if 6 <= x < 18 else 'Nighttime' if pd.notna(x) else 'Unknown'
    )
    time_of_day_counts = collision_data['time_of_day'].value_counts()
    plt.figure(figsize=(8, 5))
    time_of_day_counts.plot(kind='bar', color='purple', title="Collision Frequencies by Time of Day")
    plt.ylabel("Number of Collisions")
    plt.xlabel("Time of Day")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("includes/outputs/figures/5_collision_time_of_day_grouped.svg", format="svg")
    plt.show()

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#5 task was processed succesfully.")