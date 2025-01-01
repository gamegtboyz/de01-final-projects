===
DATA SOURCE & QUESTIONS

We gathered this information from the following link:
    https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data

Then use the code as shown in python script to fetch the data. Then, upload onto .csv files for further analysis.

The questions we primarily asked from the dataset are:
1. What are the most common cause (a.k.a contributing factor) for vehicle collision. (use top x rank)
2. Which type of vehicle are most common in collisions. (use top x rank)
3. Where are the most frequent collision site. (we will mapped the coordinates as visualization)
4. Which type of vehicle cause the most casualities/fatalities rate (person per 1000 collisions)
5. Is the time of the day (daytime/nighttime) associated with collision frequencies.


=========================
INSTALLATION GUIDE
=========================
็Here's how to install Apache Airflow through Docker Desktop, and how to maintenance it.

After install Docker Desktop, open VScode and WSL terminal and put the following command.
1. curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'    # to create .yaml file, which include the pack of software i.e. postgres, redis, and airflow.
2. mkdir -p ./dags ./logs ./plugins     # setup airflow directories
3. echo -e "AIRFLOW_UID=$(id -u)" > .env    # set up the permissions of curent user to virtual environment.


=========================
USERS' GUIDE
=========================
Right after 
1. docker-compose up airflow-init       # initialize airflow database
2. docker-compose up        # start running airflow. you could access airflow UI at this point using localhost:8080 with username == airflow and password == airflow

For users who clone this repository with Docker Desktop installed, please use the command as mentioned in 4. and 5.


=========================
MAINTENANCE GUIDE
=========================
In case of localhost:8080 doesn't load (this happended on my PC when reopen the computer), you could use theis following commands to troubleshoot the issues
1. docker restart <webserver container NAMES>       # to restart the container

in case of command per 1 doesn't work, please use the following command respectively to reinitiate the airflow
1. docker-compose down --volumes --remove-orphans
2. docker-compose up airflow-init
3. docker-compose up -d
