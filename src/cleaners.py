from src.eda import make_counter
import pandas as pd

def id_list_from_history(data):
    '''
    Takes raw data returnd by api_calls.get_match_history() and returns a list of just the match ID's
    
    Input:
        
        data(list):
            list of match objects
            
    Output:
        
        List of integers each representing a unique match id
    '''
    
    return [int(i['match_id']) for i in data]

def clean_match_details(match):
    '''
    Takes raw data from api_calls.get_match_details() and returns a dictionary with the pertinent details
    
    Input:
        
        match(dict):
            Return of the api.steampowers api
            Dict with one key-Val pair result is a dictionary with the match information
    
    Output:
        
        out(dict):
            Dictionary of pertinent data:
                radiant_win(bool): Team that won
                match_date(timestamp): When the match was played 
                radiant_hero_ids(list of ints): List of hero Ids for the radiant team 
                dire_hero_ids(list of ints): List of hero Ids for the dire team 
                
    '''
    data = match['result']
    out = {}
    out['_id'] = data['match_id']
    out['radiant_win'] = int(data['radiant_win'])
    out['match_date'] = data['start_time']
    out['radiant_hero_ids'] = []
    out['dire_hero_ids'] = []
    for player in data['players']:
        if player['player_slot'] < 128:
            out['radiant_hero_ids'] += [player['hero_id']]
        else:
            out['dire_hero_ids'] += [player['hero_id']]
    return out

def make_csv(counter, counter_data):
    '''
    Takes in a premade coutner using make_counter from eda.py and the data used to amke the counter and produces a CSV.
    
    Input:
        
        counter(Counter): 
            Counter from all the DB data - used to generate unique columns
            
        counter_data(mongo cursor list):
            return of .find() on the raw collection
        
    Output:
        
        None: Creates a csv file in the same directory as run 
    '''
    #remove count column so keys includes only hero ids
    del counter['count']
    uids = sorted(counter.keys())
    uid_cols =  []
    #add a column for each hero fro each team
    for i in uids:
        uid_cols += [(str(i)+'R')]
        uid_cols += [(str(i)+'D')]
    #add the initial 3 columns and combine with hero id columns
    columns = ['match_id', 'match_date', 'radiant_win']
    columns += uid_cols
    #create a template for each row
    row_template = {col: 0 for col in columns}
    rows_list = []
    #for each match format a row and add to list
    for match in counter_data:
        temp_row = row_template.copy()
        temp_row['match_id'] = match['_id']
        temp_row['match_date'] = match['match_date']
        temp_row['radiant_win'] = match['radiant_win']
        for indx, hid in enumerate(match['radiant_hero_ids']):
            temp_row[(str(hid)+'R')] = 1
            temp_row[(str(match['dire_hero_ids'][indx])+'D')] = 1
        rows_list += [temp_row]
    #use rows to create dataframe and print to csv
    df = pd.DataFrame(rows_list)
    df.to_csv('test.csv')
    