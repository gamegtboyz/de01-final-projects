import pandas as pd
import matplotlib.pyplot as plt
import folium

# Load the dataset
csv_file_path = "includes/outputs/nyc-collisions.csv"  # Replace with your file path
collision_data = pd.read_csv(csv_file_path)

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

# 1. Top Contributing Factors Visualization
contributing_factors = collision_data[
    ['contributing_factor_vehicle_1', 'contributing_factor_vehicle_2']
].stack().value_counts().head(10)
plt.figure(figsize=(10, 6))
contributing_factors.sort_values().plot(kind='barh', color='skyblue', title="Top Contributing Factors for Vehicle Collisions")
plt.xlabel("Number of Collisions")
plt.ylabel("Contributing Factors")
plt.tight_layout()
plt.savefig("top_contributing_factors.svg", format="svg")
plt.show()

# 2. Most Common Vehicle Types (Grouped)
vehicle_type_counts_grouped = collision_data.melt(
    value_vars=vehicle_type_columns, value_name="vehicle_type"
).dropna(subset=["vehicle_type"])['vehicle_type'].value_counts()
plt.figure(figsize=(10, 6))
vehicle_type_counts_grouped.sort_values().plot(kind='barh', color='orange', title="Most Common Vehicle Types in Collisions (Grouped)")
plt.xlabel("Number of Collisions")
plt.ylabel("Vehicle Types")
plt.tight_layout()
plt.savefig("common_vehicle_types_grouped.svg", format="svg")
plt.show()

# 4. Casualty Rates by Vehicle Type (Grouped)
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
casualty_rates_grouped['casualties_per_1000_collisions'].sort_values().plot(
    kind='barh', color='green', title="Vehicle Types with Highest Casualty Rates (Grouped)"
)
plt.xlabel("Casualties per 1,000 Collisions")
plt.ylabel("Vehicle Types")
plt.tight_layout()
plt.savefig("vehicle_casualty_rates_grouped.svg", format="svg")
plt.show()

# 5. Collision Frequencies by Time of Day
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
plt.savefig("collision_time_of_day_grouped.svg", format="svg")
plt.show()

# 3. Interactive Map for Most Frequent Collision Sites
top_collision_sites = collision_data.groupby(['latitude', 'longitude']).size().reset_index(name='collision_count')
top_collision_sites = top_collision_sites.sort_values(by='collision_count', ascending=False).head(10)
nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
for _, row in top_collision_sites.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Collisions: {row['collision_count']}"
    ).add_to(nyc_map)
nyc_map.save("nyc_collision_map.html")
