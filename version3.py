import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Chargement du jeu de données
df = pd.read_csv('https://drive.google.com/uc?export=download&id=1N3FclyWK0Hnpqla-MEbZy9KejVzNuf8V')
scattergeo = go.Scattergeo(
    lat=df['Latitude'],
    lon=df['Longitude'],
    marker=dict(color='red')
)

# Initialisation de l'application Dash
app = dash.Dash()

# Définition du layout de l'application
app.layout = html.Div([
    # Titre du tableau de bord
    html.H1('Tableau de bord avec Plotly Dash'),
    # Frise temporelle
    dcc.RangeSlider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
    # Graphique à barres
    dcc.Graph(
        id='histogram'
    ),
    # Graphique de carte
    dcc.Graph(
    id='map',
    figure={
        'data': [scattergeo],
        'layout': {
            'geo': {
                'projection': 'natural earth',
                'center': {'lat': 46.2276, 'lon': 2.2137},
            }
        }
    }
)

])

@app.callback(
    [dash.dependencies.Output('histogram', 'figure')],
    [dash.dependencies.Input('year-slider', 'value')],
)
def update_histogram(year_range):
    # Filtrage des données en fonction de la sélection de l'utilisateur sur la frise temporelle
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    # Création du graphique
    figure = {
        'data': [
            {'x': filtered_df['Year'], 'y': filtered_df.groupby('Year').size(), 'type': 'bar'},
        ],
        'layout': {
            'title': 'Nombre de séismes par année'
        }
    }
    return figure,

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)