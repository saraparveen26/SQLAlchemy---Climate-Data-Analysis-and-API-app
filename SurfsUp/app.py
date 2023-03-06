import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect the existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Welcome to SurfsUp API<br/>"
        f"_______________________<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve last 12 months of data"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value.

    # Find the most recent date in the dataset.
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= year_ago_date).\
                    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Create a dictionary using date as the key and prcp as the value
    prcp_data = []
    for date, prcp in prcp_scores:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)
    
    # Return the JSON representation of dictionary.
    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    """Get a list of stations"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the station data
    station_data = session.query(Station.name).all()
    
    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_data))
    
    # Return a JSON list of stations from the dataset.
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Get temperature data for the most active station for last year"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the dataset.
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Find the most active station id
    most_active_station = session.query(Measurement.station).\
                            group_by(Measurement.station).\
                            order_by(func.count(Measurement.station).desc()).first()
    most_active_station = most_active_station[0]

    # Perform a query to get the dates and temperature observations of the most-active station
    # for the previous year of data
    station_temp_data = session.query(Measurement.date, Measurement.tobs).\
                                filter(Measurement.station == most_active_station).\
                                filter(Measurement.date >= year_ago_date).\
                                order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    station_temp_list = list(station_temp_data)
    
    # Return a JSON list of temperature data of previous year for the most active station (USC00519281)
    return jsonify(station_temp_list)


@app.route("/api/v1.0/<start>")
def start(start):
    """Get min, max and average temperature data from start date"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create list for date and temperature values
    sel = [Measurement.date,
           func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]

    # Perform a query to get TMIN, TAVG, and TMAX for all the dates 
    # greater than or equal to the start date, taken as a parameter from the URL
    start_data = session.query(*sel).\
                    filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
                    group_by(Measurement.date).\
                    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    start_data_list = list(np.ravel(start_data))

    # Create a dictionary to store date, min, max and avg temperature values
    start_data_list1 = []
    for date, min, max, avg in start_data:
        start_dict = {}
        start_dict["date"] = date
        start_dict["min_temp"] = min
        start_dict["max_temp"] = max
        start_dict["avg_temp"] = avg
        start_data_list1.append(start_dict)
    
    # Return a JSON list of the minimum temperature, the average temperature, and the
    # maximum temperature calculated from the given start date to the end of the dataset
    return jsonify(start_data_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Get min, max and average temperature data from start date to end date"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create list for date and temperature values
    sel = [Measurement.date,
           func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]

    # Perform a query to get TMIN, TAVG, and TMAX for all the dates from start date to
    # end date inclusive, taken as parameters from the URL
    start_end_data = session.query(*sel).\
                    filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
                    filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).\
                    group_by(Measurement.date).\
                    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    start_end_data_list = list(np.ravel(start_end_data))

    # Create a dictionary to store date, min, max and avg temperature values
    start_end_data_list1 = []
    for date, min, max, avg in start_end_data:
        start_dict = {}
        start_dict["date"] = date
        start_dict["min_temp"] = min
        start_dict["max_temp"] = max
        start_dict["avg_temp"] = avg
        start_end_data_list1.append(start_dict)
    
    # Return a JSON list of the minimum temperature, the average temperature, and the
    # maximum temperature calculated from the given start date to the given end date
    return jsonify(start_end_data_list)


if __name__ == '__main__':
    app.run(debug=True)