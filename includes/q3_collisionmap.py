def collisionmap():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    import matplotlib.pyplot as plt
    import folium
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT * from collisions"

    # export query to dataframe
    collision_data = pd.read_sql_query(query, engine)

    # answer the question3: Mapping of the collisions site
    # 3. Interactive Map for Most Frequent Collision Sites
    top_collision_sites = collision_data.groupby(['latitude', 'longitude']).size().reset_index(name='collision_count')
    top_collision_sites = top_collision_sites.sort_values(by='collision_count', ascending=False).head(10)
    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
    for _, row in top_collision_sites.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Collisions: {row['collision_count']}"
        ).add_to(nyc_map)
    nyc_map.save("includes/outputs/figures/3_nyc_collision_map.html")

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#3 task was processed succesfully.")