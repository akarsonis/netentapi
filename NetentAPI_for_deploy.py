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
   
    df = json_normalize(json_dict, record_path='playersInGameRound', meta=['bet', 'dealerId', 'dealerName', 'gameOutcome', 'gameRoundDuration', 'gameRoundId', 'gameType', 'tableId', 'win'])
    
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
