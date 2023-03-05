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

# Create our session (link) from Python to the DB
session = Session(engine)

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

    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value.

    # Return the JSON representation of your dictionary.

    # Find the most recent date in the dataset.
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    latest_year_date = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= latest_year_date).all()
    
    # Create a dictionary using date s the key and prcp as the value
    prcp_data = []
    for date, prcp in prcp_scores:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    
    session.close()

    return jsonify(all_names)

