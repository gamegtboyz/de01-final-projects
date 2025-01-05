def casualityrate():
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

    # answer the question4: What is the vehicle type with most casuality rate
    # Grouped Vehicle Type Classification Function
    def classify_vehicle_type(vehicle_type):
        if isinstance(vehicle_type, str):
            vehicle_type = vehicle_type.lower()
            if "suv" in vehicle_type or "wagon" in vehicle_type:
                return "SUV"
            elif "sedan" in vehicle_type:
                return "Sedan"
            elif "truck" in vehicle_type:
                return "Truck"
            elif "bus" in vehicle_type:
                return "Bus"
            elif "bike" in vehicle_type or "e-bike" in vehicle_type:
                return "Bike"
            elif "scooter" in vehicle_type:
                return "Scooter"
            else:
                return "Other"
        return "Unknown"

    # Apply classification to vehicle type columns
    vehicle_type_columns = [
        'vehicle_type_code1', 'vehicle_type_code2', 'vehicle_type_code_3',
        'vehicle_type_code_4', 'vehicle_type_code_5'
    ]
    
    for col in vehicle_type_columns:
        collision_data[col] = collision_data[col].apply(classify_vehicle_type)

    # Create Total Casualties Column
    collision_data['total_casualties'] = (
        collision_data['number_of_persons_injured'] + collision_data['number_of_persons_killed']
    )

    # Casualty Rates by Vehicle Type (Grouped)
    vehicle_casualties_grouped = collision_data.melt(
        id_vars=['total_casualties'], value_vars=vehicle_type_columns, value_name='vehicle_type'
    ).dropna(subset=['vehicle_type'])
    casualty_rates_grouped = vehicle_casualties_grouped.groupby('vehicle_type')['total_casualties'].agg(
        total_casualties='sum', collision_count='count'
    )
    casualty_rates_grouped['casualties_per_1000_collisions'] = (
        casualty_rates_grouped['total_casualties'] / casualty_rates_grouped['collision_count']
    ) * 1000
    plt.figure(figsize=(10, 6))
    casualty_rates_grouped['casualties_per_1000_collisions'].sort_values().drop(labels='Unknown').plot(
        kind='barh', color='green', title="Vehicle Types with Highest Casualty Rates (Grouped)"
    )
    plt.xlabel("Casualties per 1,000 Collisions")
    plt.ylabel("Vehicle Types")
    plt.tight_layout()
    plt.savefig("includes/outputs/figures/4_vehicle_casualty_rates_grouped.svg", format="svg")

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#4 task was processed succesfully.")