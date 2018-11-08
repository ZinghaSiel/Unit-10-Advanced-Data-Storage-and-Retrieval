#Dependencies
import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Hawaii.Sqlite")

#Reflect an existing database into a new model
Base = automap_base()
#Reflect the tables
Base.prepare(engine, reflect=True)

#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind = engine)

#Flask Setup
App = Flask(__name__)

@app.route("/")
def Welcome():
    #Available api routes
    return (
        f"Welcome to ClimateApp!"
        f"<br/>"
        f"Available Routes:"
        f"<br/>"
        f"/api/v1.0/PrecipitationData"
        f"<br/>"
        f"/api/v1.0/StationAnalysis"
        f"<br/>"
        f"/api/v1.0/Tobs"
    )

@app.route("/api/v1.0/precipitation")
def PrecipitationData():
    session = Session(engine)

    Precipitation_Data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()

    Result = dict(Precipitation_Data)
    return jsonify(Result)

@app.route("/api/v1.0/stations")
def StationAnalysis():
    session = Session(engine)

    Station_Analysis = session.query(Measurement.station).group_by('station').all()

    Result = list(np.ravel(Station_Analysis))
    return jsonify(Result)

@app.route("/api/v1.0/tobs")
def Tobs():
    session = Session(engine)

    ID = 'USC00519281'
    Temperatures = session.query(Measurement.tobs).filter(Measurement.station == ID).\
        filter(Measurement.date >= '2016-08-23').all()

    Result = dict(zip(key,values))
    return jsonify(Result)
   
if __name__ == '__main__':
    app.run(debug=True)