import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template,request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/SQLProject2.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# print(Base.classes.keys())
# Save reference to the table
WHR = Base.classes.WHR2021

Region = Base.classes.Region_Happiness

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


################################################
# Flask Routes
#################################################


#---------------------------------
# Web Pages
#---------------------------------
@app.route("/")
def home():
  # csv_file = request.files['coordinates.csv']
  # csv_file = TextIOWrapper(csv_file, encoding='utf-8')
  # sv_reader = csv.reader(csv_file, delimiter=',')
  return render_template("index.html")

@app.route("/data")
def data_page():

  return render_template("data.html")

@app.route("/top5")
def top5_page():

  return render_template("top5.html")


# @app.route("/csv")
# def csv():
#   csv_file = request.files['coordinates.csv']
#   csv_file = TextIOWrapper(csv_file, encoding='utf-8')
#   sv_reader = csv.reader(csv_file, delimiter=',')
#   return sv_reader

#----------------------Correlation Matrix attempt


@app.route("/api/v1.0/Correlation")
def Correlation():
      session = Session(engine)

      corr = session.query(WHR.Ladder_score, WHR.Explained_by_Log_GDP_per_capita, WHR.Explained_by_Social_support, WHR.Explained_by_Healthy_life_expectancy, WHR.Explained_by_Freedom_to_make_life_choices, WHR.Explained_by_Generosity, WHR.Explained_by_Perceptions_of_corruption, WHR.Dystopia_residual).all()

      session.close()

      matrix_df = pd.DataFrame(corr)
    
      matrix = matrix_df.corr().values.tolist()
      # print(matrix)

      return jsonify(matrix)

@app.route("/api/v1.0/Region")
def Region():
      session = Session(engine)

      region_score = session.query(Region.Regional_indicator, Region.Happiness_score)


@app.route("/map")
def map_page():
      
  return render_template("map.html")



#---------------------------------
# API
#---------------------------------
@app.route("/api/v1.0/WHR2021")
def WHR2021():
    # Create our session (link) from Python to the DB
    session = Session(engine)


       # Query all passengers
    results = session.query(WHR.Country_name, WHR.Regional_indicator, WHR.Ladder_score, WHR.Healthy_life_expectancy, WHR.Explained_by_Log_GDP_per_capita, 
    WHR.Explained_by_Social_support, WHR.Explained_by_Healthy_life_expectancy, WHR.Explained_by_Freedom_to_make_life_choices,
    WHR.Explained_by_Generosity, WHR.Explained_by_Perceptions_of_corruption, WHR.Dystopia_residual, WHR.Residual_X
    ).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    WHR_all = []
    for Country_name, Regional_indicator, Ladder_score, Healthy_life_expectancy, Explained_by_Log_GDP_per_capita, Explained_by_Social_support, Explained_by_Healthy_life_expectancy, Explained_by_Freedom_to_make_life_choices, Explained_by_Generosity, Explained_by_Perceptions_of_corruption, Dystopia_residual, Residual_X in results:
        WHR_dict = {}
        WHR_dict["Country_name"] = Country_name
        WHR_dict["Regional_indicator"] = Regional_indicator
        WHR_dict["Ladder_score"] = Ladder_score
        WHR_dict["Healthy_life_expectancy"] = Healthy_life_expectancy
        WHR_dict["Explained_by_Log_GDP_per_capita"] = Explained_by_Log_GDP_per_capita
        WHR_dict["Explained_by_Social_support"] = Explained_by_Social_support
        WHR_dict["Explained_by_Healthy_life_expectancy"] = Explained_by_Healthy_life_expectancy
        WHR_dict["Explained_by_Freedom_to_make_life_choices"] = Explained_by_Freedom_to_make_life_choices
        WHR_dict["Explained_by_Generosity"] = Explained_by_Generosity
        WHR_dict["Explained_by_Perceptions_of_corruption"] = Explained_by_Perceptions_of_corruption
        WHR_dict["Dystopia_residual"] = Dystopia_residual
        WHR_dict["Residual_X"] = Residual_X
        WHR_all.append(WHR_dict)

    return jsonify(WHR_all)

if __name__ == '__main__':
    app.run(debug=True)