# Practice
## Step 2 - Climate App

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use Flask to create your routes.

### Routes

#  `/`

  # Home page.

  # List all routes that are available.

# `/api/v1.0/precipitation`

  # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  # Return the JSON representation of your dictionary.

# `/api/v1.0/stations`

    # Return a JSON list of stations from the dataset.

# `/api/v1.0/tobs`
  # Query the dates and temperature observations of the most active station for the last year of data.
  
  # Return a JSON list of temperature observations (TOBS) for the previous year.

# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Hints

# You will need to join the station and measurement tables for some of the queries.

# Use Flask `jsonify` to convert your API data into a valid JSON response object.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

# Datebase Setup
engine = create_engine("sqlite:/Resources/hawii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.stations
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

#Flask Route
@app.route("/")
def welcome():
    return""<html>
    <h1>List of all available Honolulu, HI API routes</h1>
    <ul>
    <br>
    <li>
    # Return a JSON list of stations from the dataset:
    <br>
    <a href="/api/v1.0/tobs"/api/v1.0/tobs</a>
    </li>
    <br>
    <li>
    #Return a JSON list of tmin, tmax, tavg for the dates greater than or equal to the date provided:
    <br>Replace &ltstart&gt with a date in Year-Month-Date format.
    <br>
    <a href="/api/v1.0/2-17-01-01">/api/v1.0/2017-01-01</a>
    </li>
    <br>
    <li>
    #Return a JSON list of tmin, tmax, tavg for the dates in range of start and end date:
    <br>
    Replace &ltstart&gt and &ltend&gt with a date in Year-Month-Day format.
    <br>
    <br>
    <a href="/api/v1.0/2017-01-01/2017-01-07">/api?v1.0/2017-01-01/2017-01-07</a>
    </li>
    <br>
    </ul>
    </html>


@app.route("/api/v1.0/previpitation")
def precipitation():
  # Docstring
  """Retunr a list of previpitations from last year"""
  # Design a query to retrieve the last 12 months of precipitation data and plot the results 
  max_date = session.query(Measurement.date)order_by(Measurement.date.desc()).first()

  # Get the first element of the tuple
  max_date = max_date[0]

  # Calculate the date 1 year ago from today
  # The days are eqaul 366 so that the first day of the year is included
  year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)

  # Perform a query to retrieve the data and precipitation scores
  results_precipitation = session.query(Measurement.date, Measurement.prcp)filter(Measurement.date >= year_ago).all()

  # Convert list of tuples inot normal lsit
  precipitation_dict = dict(results_precipitation)

  return jsonify(precipitation_dict)

  @app.route("/api/v1.0/stations")
  def stations():
    #Docstring
    """Return a JSON list of stations from the dataset."""
    #Query stations
    results_stations = session.query(Measurement.station).group_by(Measurement_station).all()
    # COnvert list of tuples into normal list
    station_list = list(np.ravel(results_stations))
    return jsonify(stations_list)
@app.route("/api/v1.0/tobs")
def tobs():
  #Docstring
  """Return a JSON list of Temperature Observations (tobs) for the previous year."""

  #Design a query to retrieve the last 12 months of precipitation data and plot the results
  max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

  # Get the first element of the tuple
  max_date = max_date[0]

  # Calculate the date 1 year ago from today
  # The days are equal 366 so that the first day of the year is included
  year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)
  # Query tobs
  results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()

# Convert list of tuples into normal list
tobs_list = lists(results_tobs)

return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start=None):
  # Docstring
  """Return a JSON list of tmin, tmax, tavg for the dates greater than or equal to the date provided"""

  from_start = session.query(Measurement.date), func.min(Measurement.tobs), fun.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).groupby(Measurement.date).all()
  from_start_list=list(from_start)
  return jsonify(from_start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
  # Docstring
  """Return a JSON list of tmin, tmax,tavg for the dates in range of start date and end date inclusive"""

  between_dates = session.query(Measurement.date, func.min(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).groupby(Measurement.date).all()
  between_dates_list=list(between_dates)
  return jsonify(between_dates_list)

if__name__ == '__main__':
    app.run(debug=True)  