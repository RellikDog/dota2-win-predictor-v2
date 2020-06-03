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
    out['match_id'] = data['match_id']
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