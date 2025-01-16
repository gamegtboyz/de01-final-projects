def collisionmap():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    import matplotlib.pyplot as plt
    import folium
    from folium.plugins import HeatMap
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT latitude,longitude from collisions"

    # export query to dataframe
    collision_data = pd.read_sql_query(query, engine)
    collision_data.drop(collision_data[(collision_data['latitude'] == 0) & (collision_data['longitude'] == 0)].index, inplace = True)

    # answer the question3: Mapping of the collisions site
    # build up interactive map 
    collision_sites = collision_data.groupby(['latitude', 'longitude']).size().reset_index(name='collision_count')
    top_collision_sites = collision_sites.sort_values(by='collision_count', ascending=False).head(50)
    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
    
    # Prepare data for the heatmap (latitude, longitude, and collision count)
    heat_data = [[row['latitude'], row['longitude'], row['collision_count']] for _, row in collision_sites.iterrows()]

    # Add the heatmap layer to the map
    HeatMap(heat_data, min_opacity=0.2, max_zoom=13, radius=15).add_to(nyc_map)
    
    # Add top collision site onto the chart
    for _, row in top_collision_sites.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Collisions: {row['collision_count']}"
        ).add_to(nyc_map)
    nyc_map.save("includes/outputs/figures/nyc_collision_map.html")

    # close database connection
    engine.dispose()
    query_t = "SELECT COALESCE(ON_STREET_NAME, 'Unknown') AS Collision_Street,COALESCE(CROSS_STREET_NAME, 'Unknown') AS Cross_Street,COUNT(*) AS Collision_Count FROM collisions WHERE ON_STREET_NAME IS NOT NULL OR CROSS_STREET_NAME IS NOT NULL GROUP BY COALESCE(ON_STREET_NAME, 'Unknown'), COALESCE(CROSS_STREET_NAME, 'Unknown') ORDER BY Collision_Count DESC LIMIT 10"
    collision_data_t = pd.read_sql_query(query_t, engine)
    
    collision_data_t.to_csv('includes/outputs/tables/table3.csv')


    # inform the processing results
    print("Question#3 task was processed succesfully.")