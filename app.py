from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ETL import extract, transform, load

# ETL
URL = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/lieux-de-tournage-a-paris/exports/csv'
TABLE_NAME = 'tournage_paris_table'

data = extract(URL)
data = transform(data)
load(data, TABLE_NAME)

# Figures
nbr_tournages_annee = pd.DataFrame({
    'annee' : pd.to_datetime(data['date_debut']).dt.year.value_counts().index,
    'nbr_tournages': pd.to_datetime(data['date_debut']).dt.year.value_counts().values.flatten()})
bar_nbr_tournages_annee = px.bar(nbr_tournages_annee, x='annee', y='nbr_tournages')

nbr_tournages_saison = pd.DataFrame({
    'saison' : data['saison'].value_counts().index,
    'nbr_tournages': data['saison'].value_counts().values.flatten()})
bar_nbr_tournages_saison = px.bar(nbr_tournages_saison, x='saison', y='nbr_tournages')

repartition_type_tournage = pd.DataFrame({
    'type_tournage' : data['type_tournage'].value_counts().index,
    'nbr_tournages': data['type_tournage'].value_counts().values.flatten()})
pie_repartition_type_tournage = px.pie(repartition_type_tournage, values='nbr_tournages', names='type_tournage')

# Dashboard
app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Dashboard', style={'textAlign':'center'}),
    html.Div([
        html.H1(children='Nombre de tournages par année', style={'textAlign':'center'}),
        dcc.Graph(id='bar_nbr_tournages_annee', figure=bar_nbr_tournages_annee)
    ]),

    html.Div([
        html.H1(children='Nombre de tournages par saison', style={'textAlign':'center'}),
        dcc.Graph(id='bar_nbr_tournages_saison', figure=bar_nbr_tournages_saison)
    ]),
    
    html.Div([
        html.H1(children='Répartition des types de tournage', style={'textAlign':'center'}),
        dcc.Graph(id='pie_repartition_type_tournage', figure=pie_repartition_type_tournage)
    ]),

])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
