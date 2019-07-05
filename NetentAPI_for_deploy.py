from flask import Flask, request

from sqlalchemy import create_engine
import sqlalchemy

#import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

app = Flask(__name__) #create the Flask server

@app.route('/', methods=['POST'])
def jsonexample():
    #EXTRACTING DATA
    json_dict = request.get_json()
    
    #TRANSFORMING DATA
    pd.set_option('display.expand_frame_repr', False)
    
    #cards_data = json_normalize(json_dict, record_path='cards', meta=['bet', 'dealerId', 'dealerName', 'gameOutcome', 'gameRoundDuration', 'gameRoundId', 'gameType', 'tableId', 'win'])
    df = json_normalize(json_dict, record_path='playersInGameRound', meta=['bet', 'dealerId', 'dealerName', 'gameOutcome', 'gameRoundDuration', 'gameRoundId', 'gameType', 'tableId', 'win'])
    
    #df = cards_data.merge(players_data, on=['bet', 'dealerId', 'dealerName', 'gameOutcome', 'gameRoundDuration', 'gameRoundId', 'gameType', 'tableId', 'win'], how='inner')
    #if 'cards' not in df.columns.tolist():
        #df["cards"] = np.nan
    
    #LOADING TO DB
    engine = create_engine('postgresql://postgres:uMdrmuBaFKKh8bvf@35.241.187.56:5432/')
    
    df.to_sql(
        'netent_data', 
        engine, 
        if_exists='append', 
        dtype={'bets': sqlalchemy.types.JSON, 'wins': sqlalchemy.types.JSON}, 
        index=False
    )
    engine.dispose()
    
    return 'Data was successfully saved to the Database'


if __name__ == '__main__':
    app.run(debug=True, port=5000)