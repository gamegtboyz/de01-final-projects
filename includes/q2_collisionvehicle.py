def collisionvehicle():
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
        vehicle_type_code_5\
        from collisions"

    # export query to dataframe
    collision_data = pd.read_sql_query(query, engine)

    # answer the question2: Which 10 type of vehicle are most common in collisions.
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

    # 2. Most Common Vehicle Types (Grouped)
    vehicle_type_counts_grouped = collision_data.melt(
        value_vars=vehicle_type_columns, value_name="vehicle_type"
    ).dropna(subset=["vehicle_type"])['vehicle_type'].value_counts().drop(labels='Unknown')
    plt.figure(figsize=(10, 6))
    vehicle_type_counts_grouped.sort_values().plot(kind='barh', color='orange', title="Most Common Vehicle Types in Collisions (Grouped)")
    plt.xlabel("Number of Collisions")
    plt.ylabel("Vehicle Types")
    plt.tight_layout()
    plt.savefig("includes/outputs/figures/2_common_vehicle_types_grouped.svg", format="svg")

    # close database connection
    engine.dispose()

    query_t = "SELECT mv.vehicletypecode,count(*) as frequency from (select vehicle_type_code1 vehicletypecode from collisions union all select vehicle_type_code2 vehicletypecode from collisions union all select vehicle_type_code_3 vehicletypecode from collisions union all select vehicle_type_code_4 vehicletypecode from collisions union all select vehicle_type_code_5 vehicletypecode from collisions  ) mv group by vehicletypecode order by frequency desc limit 10"
    collision_data_t = pd.read_sql_query(query_t, engine)
    
    collision_data_t.to_csv('includes/outputs/tables/table2.csv')

    # inform the processing results
    print("Question#2 task was processed succesfully.")