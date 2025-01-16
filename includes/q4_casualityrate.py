def casualityrate():
    # download the relevant library
    from sqlalchemy import create_engine
    import pandas as pd
    import matplotlib.pyplot as plt
    from config.db_config import connection_string

    #create database connection 
    engine = create_engine(connection_string)

    # create SQL query
    query = "SELECT \
        vehicle_type_code1,\
        vehicle_type_code2,\
        vehicle_type_code_3,\
        vehicle_type_code_4,\
        vehicle_type_code_5,\
        number_of_persons_injured,\
        number_of_persons_killed\
         from collisions"

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



    query_t = "WITH classified_vehicle_types AS (\
                SELECT \
                    collision_id,\
                    total_casualties,\
                    CASE\
                        WHEN LOWER(vehicle_type_code1) LIKE '%suv%' OR LOWER(vehicle_type_code1) LIKE '%wagon%' THEN 'SUV'\
                        WHEN LOWER(vehicle_type_code1) LIKE '%sedan%' THEN 'Sedan'\
                        WHEN LOWER(vehicle_type_code1) LIKE '%truck%' THEN 'Truck'\
                        WHEN LOWER(vehicle_type_code1) LIKE '%bus%' THEN 'Bus'\
                        WHEN LOWER(vehicle_type_code1) LIKE '%bike%' OR LOWER(vehicle_type_code1) LIKE '%e-bike%' THEN 'Bike'\
                        WHEN LOWER(vehicle_type_code1) LIKE '%scooter%' THEN 'Scooter'\
                        WHEN vehicle_type_code1 IS NOT NULL THEN 'Other'\
                        ELSE 'Unknown'\
                    END AS vehicle_type\
                FROM (\
                    SELECT *,\
                        (number_of_persons_injured + number_of_persons_killed) AS total_casualties\
                    FROM collisions\
                ) \
                UNION ALL\
                SELECT \
                    id,\
                    total_casualties,\
                    CASE\
                        WHEN LOWER(vehicle_type_code2) LIKE '%suv%' OR LOWER(vehicle_type_code2) LIKE '%wagon%' THEN 'SUV'\
                        WHEN LOWER(vehicle_type_code2) LIKE '%sedan%' THEN 'Sedan'\
                        WHEN LOWER(vehicle_type_code2) LIKE '%truck%' THEN 'Truck'\
                        WHEN LOWER(vehicle_type_code2) LIKE '%bus%' THEN 'Bus'\
                        WHEN LOWER(vehicle_type_code2) LIKE '%bike%' OR LOWER(vehicle_type_code2) LIKE '%e-bike%' THEN 'Bike'\
                        WHEN LOWER(vehicle_type_code2) LIKE '%scooter%' THEN 'Scooter'\
                        WHEN vehicle_type_code2 IS NOT NULL THEN 'Other'\
                        ELSE 'Unknown'\
                    END AS vehicle_type\
                FROM (\
                    SELECT *,\
                        (number_of_persons_injured + number_of_persons_killed) AS total_casualties\
                    FROM collisions\
                ) \
                UNION ALL\
                SELECT \
                    collision_id,\
                    total_casualties,\
                    CASE\
                        WHEN LOWER(vehicle_type_code_3) LIKE '%suv%' OR LOWER(vehicle_type_code_3) LIKE '%wagon%' THEN 'SUV'\
                        WHEN LOWER(vehicle_type_code_3) LIKE '%sedan%' THEN 'Sedan'\
                        WHEN LOWER(vehicle_type_code_3) LIKE '%truck%' THEN 'Truck'\
                        WHEN LOWER(vehicle_type_code_3) LIKE '%bus%' THEN 'Bus'\
                        WHEN LOWER(vehicle_type_code_3) LIKE '%bike%' OR LOWER(vehicle_type_code_3) LIKE '%e-bike%' THEN 'Bike'\
                        WHEN LOWER(vehicle_type_code_3) LIKE '%scooter%' THEN 'Scooter'\
                        WHEN vehicle_type_code_3 IS NOT NULL THEN 'Other'\
                        ELSE 'Unknown'\
                    END AS vehicle_type\
                FROM (\
                    SELECT *,\
                        (number_of_persons_injured + number_of_persons_killed) AS total_casualties\
                    FROM collisions\
                ) \
                UNION ALL\
                SELECT \
                    collision_id,\
                    total_casualties,\
                    CASE\
                        WHEN LOWER(vehicle_type_code_4) LIKE '%suv%' OR LOWER(vehicle_type_code_4) LIKE '%wagon%' THEN 'SUV'\
                        WHEN LOWER(vehicle_type_code_4) LIKE '%sedan%' THEN 'Sedan'\
                        WHEN LOWER(vehicle_type_code_4) LIKE '%truck%' THEN 'Truck'\
                        WHEN LOWER(vehicle_type_code_4) LIKE '%bus%' THEN 'Bus'\
                        WHEN LOWER(vehicle_type_code_4) LIKE '%bike%' OR LOWER(vehicle_type_code_4) LIKE '%e-bike%' THEN 'Bike'\
                        WHEN LOWER(vehicle_type_code_4) LIKE '%scooter%' THEN 'Scooter'\
                        WHEN vehicle_type_code_4 IS NOT NULL THEN 'Other'\
                        ELSE 'Unknown'\
                    END AS vehicle_type\
                FROM (\
                    SELECT *,\
                        (number_of_persons_injured + number_of_persons_killed) AS total_casualties\
                    FROM collisions\
                ) \
                UNION ALL\
                SELECT \
                    collision_id,\
                    total_casualties,\
                    CASE\
                        WHEN LOWER(vehicle_type_code_5) LIKE '%suv%' OR LOWER(vehicle_type_code_5) LIKE '%wagon%' THEN 'SUV'\
                        WHEN LOWER(vehicle_type_code_5) LIKE '%sedan%' THEN 'Sedan'\
                        WHEN LOWER(vehicle_type_code_5) LIKE '%truck%' THEN 'Truck'\
                        WHEN LOWER(vehicle_type_code_5) LIKE '%bus%' THEN 'Bus'\
                        WHEN LOWER(vehicle_type_code_5) LIKE '%bike%' OR LOWER(vehicle_type_code_5) LIKE '%e-bike%' THEN 'Bike'\
                        WHEN LOWER(vehicle_type_code_5) LIKE '%scooter%' THEN 'Scooter'\
                        WHEN vehicle_type_code_5 IS NOT NULL THEN 'Other'\
                        ELSE 'Unknown'\
                    END AS vehicle_type\
                FROM (\
                    SELECT *,\
                        (number_of_persons_injured + number_of_persons_killed) AS total_casualties\
                    FROM collisions\
                ) \
            )\
            SELECT \
                vehicle_type,\
                SUM(total_casualties) AS total_casualties,\
                COUNT(*) AS collision_count,\
                (SUM(total_casualties) * 1000.0 / COUNT(*)) AS casualties_per_1000_collisions\
            FROM classified_vehicle_types\
            WHERE vehicle_type <> 'Unknown'\
            GROUP BY vehicle_type\
            ORDER BY casualties_per_1000_collisions DESC;"
    
    
    collision_data_t = pd.read_sql_query(query_t, engine)
    
    collision_data_t.to_csv('includes/outputs/tables/table4.csv')

    # close database connection
    engine.dispose()

    # inform the processing results
    print("Question#4 task was processed succesfully.")