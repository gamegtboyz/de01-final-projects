FROM apache/airflow:2.10.4

# Install matplotlib and relevant package to Docker Image
RUN pip install matplotlib
RUN pip install folium