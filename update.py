import time
import requests
import pymongo
import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dota_data
from src.api_calls import get_match_history, get_match_details
from src.cleaners import id_list_from_history, clean_match_details, make_csv, make_pred_row
from src.populate_db import populate_db
from src.heroes import heroes, name_id, id_name
from src.eda import make_counter
from src.models import train_rfc
import pandas as pd
import numpy as np
from datetime import datetime

def pop_n_remake():
    populate_db()
    c = make_counter(db.raw.find())
    make_csv(c, db.raw.find())
    time.sleep(120)
    train_rfc(pd.read_csv('test.csv'))
    
    

def main():
    """runs infinte loop checking time and running pop n remake dunring set times."""
    while True:
        hour = int(str(datetime.now().time())[:2])
        print(hour)
        if hour < 2:
            try:
                pop_n_remake()
            except:
                'Error something ent wrong witht he DB popluation and csv or pickle making'
            time.sleep(7200)
        else:
            print('its not time')
            time.sleep(7190)


if __name__ == "__main__":
    main()
    

