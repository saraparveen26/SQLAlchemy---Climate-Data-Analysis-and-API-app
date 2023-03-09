# SurfsUP - Climate Data Analysis and Climate API app

This challenge is completed as requirement of Data Analytics Boot Camp at University of Toronto

The project analyzes the Climate and Station data for holiday destination of Honolulu, Hawaii in order to plan a vacation. The project performs climate analysis about the area by exploring climate data and creating an app.

## Part 1: Analyze and Explore the Climate Data

This section of the project uses Python and SQLALchemy to do a basic climate analysis and data exploration of the SQLite climate database by using ORM queries, Pandas and Matplotlib. This is achieved by using SQLAlchemy functions of create_engine() and automap_base() to connect to the database and reflect the tables into classes respectively. There are two classes in this database named 'station' and 'measurement'. The data is then explored by creating session, performing queries and then closing the session.

### *Precipitation Analysis:*

The first part of the analysis includes precipitation data. This includes the following steps:

1. Finding the most recent date in the dataset.

2. Getting previous 12 months of precipitation data by using the most recent date by performing query.

3. Loading the query results into a Pandas DataFrame and setting index to 'date' column and sorting it.

4. Plotting the results using 'plot' method which creates the following chart:

![alt text](SurfsUp/Images/Fig1.png)
