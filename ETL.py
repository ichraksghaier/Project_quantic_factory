import requests
from io import StringIO
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import yaml
from utils import get_season


# récupération des données par API
def extract(url):
    try:
        response = requests.get(url)
        data = pd.read_csv(StringIO(response.text, newline=''), sep=';')
        return data
    except Exception as e:
        print('Data extraction error' + str(e))

# transformation des données
def transform(data):
    try:
        # supprimer les colonnes vides.
        data = data.drop(['created_user', 'created_date', 'last_edited_user', 'last_edited_date'], axis=1)
        # Ajouter une nouvelle colonne pour la saison
        data["saison"] = pd.to_datetime(data['date_debut']).dt.month.apply(get_season)
        return data
    except Exception as e:
        print('Data transformation error' + str(e))

# chargement des données
def load(data, table_name):
    try:
        with open("config.yaml", "r") as configfile:
             config = yaml.load(configfile, Loader=yaml.FullLoader)
        configfile.close()
        username = config['Database']['username']
        pwd = config['Database']['pwd']
        host = config['Database']['host']
        port = int(config['Database']['port'])
        db = config['Database']['db']

        engine = create_engine(f'mysql+pymysql://{username}:{pwd}@{host}:{port}/{db}')
        if not database_exists(engine.url): 
            create_database(engine.url)

        rows_imported = 0
        print(f'importing rows: row {rows_imported} to {rows_imported + len(data)}...')
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        rows_imported += len(data)
        print('data imported successfully')
    except Exception as e:
        print('Data loading error' + str(e))
