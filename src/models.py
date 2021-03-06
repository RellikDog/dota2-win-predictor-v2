import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

def train_rfc(df):
    '''
    Trains Random forest Clasifier using DF made from make_csv's csv file - Deatail on how the hyperparamaters were picked cand the modela can be found here :  https://github.com/RellikDog/dota2-win-predictor
    
    Input:
        
        df(pandasDF):
            
            A DF generated by reading in a stored CSV -EX: data = pd.read_csv('test.csv') -> train_rfc(data) 
    
    Output:
        
        None:
            Generates a .pkl file named rfc.pkl with the RFC model.
    '''
    drop_cols = ['Unnamed: 0', 'match_id', 'match_date', 'Unnamed: 1']
    for i in drop_cols:
        try:
            df.pop(i)
        except:
            continue
    trf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                       max_depth=None, max_features='sqrt', max_leaf_nodes=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=4, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, n_estimators=300,
                       n_jobs=None, oob_score=False, random_state=1, verbose=0,
                       warm_start=False)
    y = df.pop('radiant_win')
    X = df
    trf.fit(X, y)
    pickle.dump(trf, open('rfc.pkl', 'wb'))

    
def rfc_pred(pred_row):
    '''
    Return prediction based on stored model
    
    Input:
        
        pred_row(Pandas DF):
            row to predict - generated by cleaners.make_pred_row()
            
    Output:
    
        Str - Message naming the winning team
        
    '''
    model = pickle.load(open('rfc.pkl', 'rb'))
    prediction = model.predict(pred_row)
    if prediction[0] == 1:
        return 'Radiant Team Win'
    else:
        return 'Dire Team Win'