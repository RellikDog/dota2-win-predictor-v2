from collections import Counter
import sys
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dota_data

def make_counter(data):
    '''
    Makes a Counter and loads data from the mongo DB - Prints matches with errors
    
    Input:
    
        data(mongo cursor list):
            return of .find() on the raw collection
    
    Output:
    
        c(Counter):
            Counter of hero ids as keys and the number of times they were picked - count k is number of matches processed.
    '''
    c = Counter()
    for match in data:
        c['count'] += 1
        try:
            for indx, hero_id in enumerate(match['radiant_hero_ids']):
                c[hero_id] += 1
                c[match['dire_hero_ids'][indx]] += 1
        except:
            print(match)
            try:
                match = clean_match_details(get_match_details(match['_id']))
                for indx, hero_id in enumerate(match['radiant_hero_ids']):
                    c[hero_id] += 1
                    c[match['dire_hero_ids'][indx]] += 1
                db.raw.update_one({'_id':match['_id']}, {"$set": match}, upsert=True)
            except:
                print(f'Error: {sys.exc_info()[0]}')
    return c