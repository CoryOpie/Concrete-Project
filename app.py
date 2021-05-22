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
        if request.form["Cement"]:
          cement = request.form["Cement"]
        else:
          cement = 0
        if request.form["BlastFurnaceSlag"]:
          blastfurnaceslag = request.form["BlastFurnaceSlag"]
        else:
          blastfurnaceslag = 0
        if request.form["FlyAsh"]:
          flyash = request.form["FlyAsh"]
        else:
          flyash = 0
        if request.form["Water"]:
          water = request.form["Water"]
        else:
          water = 0
        if request.form["Superplasticizer"]:
          superplasticizer = request.form["Superplasticizer"]
        else:
          superplasticizer = 0
        if request.form["CoarseAggregate"]:
          coarseaggregate = request.form["CoarseAggregate"]
        else:
          coarseaggregate = 0
        if request.form["FineAggregate"]:
          fineaggregate = request.form["FineAggregate"]
        else:
          fineaggregate = 0
        if request.form["Age"]:
          age = request.form["Age"]
        else:
          age = 1
        
        
        custinput = [[cement, blastfurnaceslag, flyash, water, superplasticizer, coarseaggregate, fineaggregate, age]]

        scaler = joblib.load("concrete2.sav")

        from sklearn.preprocessing import StandardScaler
        custinputscaled = scaler.transform(custinput)



        from tensorflow.keras.models import load_model
        model = load_model("maeConcrete.h5")

        custfinalpredict = model.predict(custinputscaled)
        print(custfinalpredict[0][0])


        predictions = round(custfinalpredict[0][0],2)

        predictionshigh = None
        predictionscommercial = None
        predictionsresidential = None
        predictionsfail = None

        if predictions > 70:
              predictionshigh = predictions
        elif predictions > 28:
              predictionscommercial = predictions
        elif predictions > 17:
              predictionsresidential = predictions
        else:
              predictionsfail = predictions
        # if predictions > 80:
        #   predictions = f'<span style= "color:green;">{predictions}</span>'
        # elif predictions >40:
        #   predictions = f'<span style= "color:yellow;">{predictions}</span>'
        # else:
        #   predictions = f'<span style= "color:red;">{predictions}</span>'


    print(predictions)
    return render_template("index.html", predictionshigh = predictionshigh, predictionsresidential = predictionsresidential, predictionscommercial = predictionscommercial, predictionsfail = predictionsfail)

if __name__ == "__main__":
    app.run()
