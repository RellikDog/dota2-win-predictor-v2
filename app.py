#=================================================================================================================================
#                                               Imports
#=================================================================================================================================
from flask import Flask, request, render_template, jsonify
from src.api_calls import get_match_history, get_match_details
from src.cleaners import id_list_from_history, clean_match_details, make_csv, make_pred_row
from src.populate_db import populate_db
import requests
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dota_data
from src.heroes import heroes, name_id, id_name
from src.eda import make_counter
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.models import train_rfc, rfc_pred
import numpy as np
import pickle
app = Flask(__name__)
#=================================================================================================================================
#                                                     Routes
#=================================================================================================================================

#Home Route
@app.route('/', methods=['GET'])
def index():
    return render_template('win-predictor.html')

#Route to solve predictions
@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    a1 = user_data['a1']
    a2 = user_data['a2']
    a3 = user_data['a3']
    a4 = user_data['a4']
    a5 = user_data['a5']
    b1 = user_data['b1']
    b2 = user_data['b2']
    b3 = user_data['b3']
    b4 = user_data['b4']
    b5 = user_data['b5']
    team_a = [a1, a2, a3, a4, a5]#Radiant
    team_b = [b1, b2, b3, b4, b5]#Dire
    prediction = pred(team_a, team_b)
    return jsonify({'prediction': prediction})

def pred(a, b):
    pred_row = make_pred_row(pd.read_csv('test.csv'), a, b)
    return rfc_pred(pred_row)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)