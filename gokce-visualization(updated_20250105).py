import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

# Load the dataset
csv_file_path = "includes/outputs/nyc-collisions.csv"  # Replace with your file path
collision_data = pd.read_csv(csv_file_path)
collision_data.drop(collision_data[(collision_data['latitude'] == 0) & (collision_data['longitude'] == 0)].index, inplace = True)

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
contributing_factors = collision_data[['contributing_factor_vehicle_1', 'contributing_factor_vehicle_2', 'contributing_factor_vehicle_3', 'contributing_factor_vehicle_4', 'contributing_factor_vehicle_5']].stack().value_counts().drop(labels='Unspecified').head(10)
plt.figure(figsize=(10, 6))
contributing_factors.sort_values().plot(kind='barh', color='skyblue', title="Top Contributing Factors for Vehicle Collisions")
plt.xlabel("Number of Collisions")
plt.ylabel("Contributing Factors")
plt.tight_layout()
plt.savefig("1_top_contributing_factors.svg", format="svg")
plt.show()

# 2. Most Common Vehicle Types (Grouped)
vehicle_type_counts_grouped = collision_data.melt(
    value_vars=vehicle_type_columns, value_name="vehicle_type"
).dropna(subset=["vehicle_type"])['vehicle_type'].value_counts().drop(labels='Unknown')
plt.figure(figsize=(10, 6))
vehicle_type_counts_grouped.sort_values().plot(kind='barh', color='orange', title="Most Common Vehicle Types in Collisions (Grouped)")
plt.xlabel("Number of Collisions")
plt.ylabel("Vehicle Types")
plt.tight_layout()
plt.savefig("2_common_vehicle_types_grouped.svg", format="svg")
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
casualty_rates_grouped['casualties_per_1000_collisions'].sort_values().drop(labels='Unknown').plot(
    kind='barh', color='green', title="Vehicle Types with Highest Casualty Rates (Grouped)"
)
plt.xlabel("Casualties per 1,000 Collisions")
plt.ylabel("Vehicle Types")
plt.tight_layout()
plt.savefig("4_vehicle_casualty_rates_grouped.svg", format="svg")
plt.show()

# 5. Collision Frequencies by Time of Day
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
plt.savefig("5_collision_time_of_day_grouped.svg", format="svg")
plt.show()

# 3. Interactive Map for Most Frequent Collision Sites
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
nyc_map.save("3_nyc_collision_map.html")
