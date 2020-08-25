import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)


Measurement = Base.classes.measurement
Station = Base.classes.station

session =Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    print("server request from home page")
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # session =Session(engine)
    previous_year = dt.date(2017, 8, 23)- dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()
    precip ={date: prcp for date, prcp in precipitation}
    # session.close()
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    #return a list of stations.
    result= session.query(Station.station).all()
    #unravel results into a 1D array and convert to a list
    stations =list(np.ravel(result))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(Measurement.tobs).filter(Measurement.station =='USC00519281').\
        filter(Measurement.date >= previous_year).all()
    temps = list(np.ravel(result))

    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start =None, end = None):

    sel =[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end: 
        result = session.query(*sel).filter(Measurement.date >= start).all()

        temps = list(np.ravel(result))
        return jsonify(temps)

    result = session.query(*sel).filter(Measurement.date >=start).\
        filter(Measurement.date <=end).all()
    temps = list(np.ravel(result))
    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)