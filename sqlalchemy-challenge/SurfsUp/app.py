# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
def main():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()
    prcp_query_dict = dict(prcp_query)
    session.close()
    return jsonify(prcp_query_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.station,Station.name).all()
    station_names_dict = dict(station_names)
    session.close()
    return jsonify(station_names_dict)
    

@app.route("/api/v1.0/tobs")
def tobs():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    #session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= previous_year).all()
    tobs = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date >= previous_year).all()
    tobs_dict = dict(tobs)
    session.close()
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    start_range_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    

    """ tobs_results = []

    for min,avg,max in start_range_query:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_results.append(tobs_dict)"""
#List comprehension version of code used above#
    tobs_results = [
        {"Min": min_temp, "Average": avg_temp, "Max": max_temp}
        for min_temp, avg_temp, max_temp in start_range_query
    ]
    
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    start_end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    start_end_results = [
        {"Min": min_temp, "Average": avg_temp, "Max": max_temp}
        for min_temp, avg_temp, max_temp in start_end_query
    ]

    return jsonify(start_end_results)
if __name__ == '__main__':
    app.run(debug=True)







