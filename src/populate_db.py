from src.api_calls import get_match_history, get_match_details
from src.cleaners import id_list_from_history, clean_match_details
import sys
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dota_data

def populate_db(runs=1, IDs_less_than=None):
    '''
    Function to automatically make querries for pro match IDs, then make a querry for each matches details, clean the details and add them to a mongo database.
    
    Input:
        
        runs(int): optional
            Number of times to draw list of match IDs.  Each run brings in 100 more IDs. (i.e. 1 run tries to insert 100 matches to the DB)
            
        IDs_less_than(int or None): optional
            Id to start at.  Leave blank to start from most recent. ID will not be included in return list of IDs.
            
    Output:
        
        None:
            Function inserts match objects into MongoDB no return
            
            Prints errors
    
    '''
    #Match ID set to none to start at begining otherwise starts after ID
    if IDs_less_than == None: 
        match_IDs = None
    else:
        match_IDs = [IDs_less_than]
    #counter to break loop if too many reinserts
    #For as many runs as were specified
    for i in range(runs):
        print(f'Run: {i+1}')
        #call pro matches api - if list of match id's use lowest match id as last id
        #get list of match id's
        if match_IDs == None:
            match_IDs = id_list_from_history(get_match_history())
        else:
            match_IDs = id_list_from_history(get_match_history(match_IDs[-1]))
        duplicates = 0
        for match_id in match_IDs:
            try:
                #insert just match id to check for duplicates
                db.raw.insert_one({'_id': match_id})
                #call & clean match detail api
                match = clean_match_details(get_match_details(match_id))
                #add data to db
                db.raw.update_one({'_id':match['_id']}, {"$set": match}, upsert=True)
                #print(f'Match {match_id} inserted')
            except pymongo.errors.DuplicateKeyError:
                print('Match ID was already in the DB')
                duplicates += 1
                if duplicates > 10:
                    break
            except:
                print(f'Unknown Error: {sys.exc_info()[0]}')
        if duplicates > 10:
            break