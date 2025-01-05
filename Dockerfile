FROM apache/airflow:2.10.4

# Install matplotlib
RUN pip install matplotlib
RUN pip install folium
RUN pip install geopandasdocker