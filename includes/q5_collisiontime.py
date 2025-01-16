def collisiontime():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    import matplotlib.pyplot as plt
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT crash_time from collisions"

    # export query to dataframe
    collision_data = pd.read_sql_query(query, engine)

    # answer the question5: Is the time of the day associated with collision frequencies.
    collision_data['crash_time'] = pd.to_datetime(collision_data['crash_time'], format='%H:%M', errors='coerce')
    collision_data['time_period'] = collision_data['crash_time'].apply(
        lambda x: 'Daytime' if 6 <= x.hour < 18 else 'Nighttime' if pd.notnull(x) else None
    )

    # Count collisions by hour for each time period
    collision_data['hour'] = collision_data['crash_time'].dt.hour
    daytime_data = collision_data[collision_data['time_period'] == 'Daytime']
    nighttime_data = collision_data[collision_data['time_period'] == 'Nighttime']

    # Prepare data for histogram
    daytime_counts = daytime_data['hour'].value_counts().sort_index()
    nighttime_counts = nighttime_data['hour'].value_counts().sort_index()

    # Create a multi-layered histogram
    plt.figure(figsize=(12, 6))
    plt.hist(daytime_data['hour'].dropna(), bins=12, range=(0, 23), alpha=0.6, label='Daytime', color='orange')
    plt.hist(nighttime_data['hour'].dropna(), bins=12, range=(0, 23), alpha=0.6, label='Nighttime', color='blue')

    # Add labels, legend, and title
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Number of Collisions', fontsize=12)
    plt.title('Multi-layered Histogram of Collisions: Daytime vs. Nighttime', fontsize=14)
    plt.legend()
    plt.xticks(range(0, 24, 2))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("includes/outputs/figures/5_collision_time_of_day_grouped.svg", format="svg")


    query_t = "WITH processed_data AS (\
                SELECT \
                    *,\
                    EXTRACT(HOUR FROM TO_TIMESTAMP(crash_time, 'HH24:MI')) AS crash_hour,\
                    CASE\
                        WHEN TO_TIMESTAMP(crash_time, 'HH24:MI')::TIME >= TIME '06:00' \
                            AND TO_TIMESTAMP(crash_time, 'HH24:MI')::TIME < TIME '18:00' THEN 'Daytime'\
                        WHEN TO_TIMESTAMP(crash_time, 'HH24:MI')::TIME IS NOT NULL THEN 'Nighttime'\
                        ELSE NULL\
                    END AS time_period\
                FROM collisions\
            ),\
            daytime_data AS (\
                SELECT \
                    crash_hour, \
                    COUNT(*) AS collision_count\
                FROM processed_data\
                WHERE time_period = 'Daytime'\
                GROUP BY crash_hour\
                ORDER BY crash_hour\
            ),\
            nighttime_data AS (\
                SELECT \
                    crash_hour, \
                    COUNT(*) AS collision_count\
                FROM processed_data\
                WHERE time_period = 'Nighttime'\
                GROUP BY crash_hour\
                ORDER BY crash_hour\
            )\
            SELECT \
                'Daytime' AS time_period, \
                crash_hour, \
                collision_count\
            FROM daytime_data\
            UNION ALL\
            SELECT \
                'Nighttime' AS time_period, \
                crash_hour, \
                collision_count\
            FROM nighttime_data\
            ORDER BY time_period, crash_hour;"

    collision_data_t = pd.read_sql_query(query_t, engine)
    
    collision_data_t.to_csv('includes/outputs/tables/table5.csv')

    # close database connection
    engine.dispose()    
    
    # inform the processing results
    print("Question#5 task was processed succesfully.")