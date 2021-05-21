# import necessary libraries
# from models import create_classes
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import pandas as pd
import joblib

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)



# engine = create_engine("sqlite:///db.sqlite")

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# # Save reference to the table
# Pet = Base.classes.pets

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################

# from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/predict", methods=["GET", "POST"])
def send():

    # session = Session(engine)

    if request.method == "POST":
        print(request.form)
        cement = request.form["Cement"]
        blastfurnaceslag = request.form["BlastFurnaceSlag"]
        flyash = request.form["FlyAsh"]
        water = request.form["Water"]
        superplasticizer = request.form["Superplasticizer"]
        coarseaggregate = request.form["CoarseAggregate"]
        fineaggregate = request.form["FineAggregate"]
        age = request.form["Age"]
        
        
        custinput = [[cement, blastfurnaceslag, flyash, water, superplasticizer, coarseaggregate, fineaggregate, age]]

        scaler = joblib.load("concrete2.sav")

        from sklearn.preprocessing import StandardScaler
        custinputscaled = scaler.transform(custinput)



        from tensorflow.keras.models import load_model
        model = load_model("maeConcrete.h5")

        custfinalpredict = model.predict(custinputscaled)
        print(custfinalpredict[0][0])

    return render_template("index.html", predictions = custfinalpredict[0][0])


if __name__ == "__main__":
    app.run()
