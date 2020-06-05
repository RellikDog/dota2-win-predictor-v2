import requests

def get_match_history(less_then_match_id=None):
    """
    Makes api call to open dota pro matches route
    Returns list of 100 match result objects
    If a match Id is provided 100 matches before specified match are returned
        
    Input:
            
        None: Retruns 100 most recent matches
            or
        less_then_match_id(int): Id of match to retrun results before
            
    Output:
            
        data(list): list of match objects(docs at https://docs.opendota.com/#tag/pro-matches)
    """
    if less_then_match_id == None:
        response = requests.get('https://api.opendota.com/api/proMatches')
    else:
        response = requests.get(f'https://api.opendota.com/api/proMatches?less_than_match_id={less_then_match_id}')
    #print(response)
    data = response.json()
    #print(data)
    return data

def get_match_details(match_id):
    '''
    Makes api call to steam api to get match details
    
    Input:
    
        match_id(int):
            id of match to get details about
    
    Output:
    
        data(dictionary): 
            Dictionary of match details
            data['result']: dictionary of results
            data['result']['players']: list of player objects
            data['result']['ratient_win']: match winner
            data['result']['start_time']: match start time as a timestamp - decode with:
                from datetime import datetime
                ts = 1591119168
                x = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    '''
    
    key = 'F5FC7EFDA058ACFD73B657E00676FEC2'
    payload = {'match_id': match_id, 'key': key}
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
    response = requests.get(api_url, params=payload)
    data = response.json()
    return data