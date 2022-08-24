# 9.5.1 setup the weather app

## import dependancies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

## setup the db connection
engine = create_engine("sqlite:///hawaii.sqlite")

## reflect the db into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

## reference the tbls 
Measurement = Base.classes.measurement
Station = Base.classes.station

## create a py/db link
session = Session(engine)

## setup flask connection
## `__name__` value depends on where/how the code is run
app = Flask(__name__)


# 9.5.2 create the welcome route

## define the root
@app.route("/")

## create the function with a return stmt
def welcome():
    return(
## add more routes (precip, stations, tobs, and stats)
## `/api/v1.0/route` is the subdirectory of the local URL
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

## define the precip route and function
### `.\` tells the query to continue on the next line
### `jsonfy()` formats the result into JSON
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


## define the station route and function
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


## define the tobs route and function
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


## define the statistics (min,max.avg temps) route and function
### when two routes are defined, params for start and end are also needed
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
### use if-not to determine the start/end dates
### `(*sel)` asterisk indicates multiple results
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
### calculate
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)