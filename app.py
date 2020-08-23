import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)


Measurement = Base.classes.measurement
Station = Base.classes.station

# session =Session(engine)

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
    session =Session(engine)
    previous_year = dt.date(2017, 8, 23)- dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()
    precip ={date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

# @app.route("/api/v1.0/stations")
# def stations():
#     #return a list of stations.
#     result= session.query(Station.station).all()
#     #unravel results into a 1D array and convert to a list
#     stations =list(np.ravel(result))
#     return jsonify(stations)

# @app.route("/api/v1.0/tobs")



# @app.route("/api/v1.0/temp/start/end")



if __name__ == "__main__":
    app.run(debug=True)