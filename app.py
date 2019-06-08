import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
def home():
    
    return (
        f"<h3>Hawaii Climate Analysis</h3>"
        f"<h4>Available Routes:</h4> <br>"
        f"/api/v1.0/precipitation <br>Returns precipitation results by date.<br><br>"
        f"/api/v1.0/stations <br>Returns active weather stations.<br><br>"
        f"/api/v1.0/tobs <br>Returns temperature observations from a total year previous to final available observation.<br><br>"
        f"/api/v1.0/<start> <br>Returns the minimum temperature, the average temperature, and the max temperature for a range of dates greater than and equal to start. <br>Use /yyyy-mm-dd format.<br><br>"
        f"/api/v1.0/<start>/<end> <br>Returns the minimum temperature, the average temperature, and the max temperature for a given start-end range. <br>Use /yyyy-mm-dd/yyyy-mm-dd format.<br><br>" 
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation **Problem with one_yr_ago variable**
    prcp_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station():
    # Query list of weather stations 
    station_list = session.query(Station.id, Station.station, Station.name).all()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query temperature observations 
    one_yr_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_yr = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date > one_yr_ago).all()

    return jsonify(tobs_yr)

@app.route("/api/v1.0/<start>")
def start(start):
    # Query temperature observations 
    start_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    return jsonify(start_calc)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    # Query temperature observations 
    start_end_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(start_end_calc)

if __name__ == '__main__':
    app.run(debug=True)