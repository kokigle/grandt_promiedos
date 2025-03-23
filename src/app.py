import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import flask

# Cargar datos
file_path = 'GRANDT_FINAL.csv'
df = pd.read_csv(file_path)

# Asegurar que los nombres de columnas sean correctos
df.columns = ["Equipo", "Jugador", "Posición", "Link", "Minutos", "Goles", "Goles/90 Hist", "Minutos 2025", "Goles 2025", "Goles/90 2025"]

# Inicializar aplicación Dash
app = flask.Flask(__name__)
server = app.server
app = dash.Dash(__name__, server=server)

# Estilos mejorados
green_style = {
    'backgroundColor': '#1a7f3d',
    'color': 'white',
    'textAlign': 'center',
    'padding': '20px',
    'fontSize': '32px',
    'fontWeight': 'bold',
    'borderRadius': '10px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
}

table_style = {
    'backgroundColor': '#f0f8f0',
    'color': 'black',
    'textAlign': 'center',
    'border': '1px solid #d1d1d1',
    'borderRadius': '8px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
}

table_header_style = {
    'backgroundColor': '#006400',
    'color': 'white',
    'fontWeight': 'bold',
    'textAlign': 'center',
    'fontSize': '18px'
}

app.layout = html.Div([
    html.H1("GRANDT PROMIEDOS", style=green_style),
    
    dash_table.DataTable(
        id='data-table',
        columns=[
            {'name': col, 'id': col, 'deletable': False, 'selectable': True, 'type': 'numeric' if "Minutos" in col or "Goles" in col else 'text'}
            for col in df.columns
        ],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        style_header=table_header_style,
        style_cell=table_style,
        style_table={'overflowX': 'auto', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'},
        style_data={'borderBottom': '1px solid #d1d1d1'},
        style_data_conditional=[
            {
                'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} > 0.5'},
                'backgroundColor': '#e6ffcc',
                'color': 'black'
            },
            {
                'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} <= 0.5'},
                'backgroundColor': '#ffe6e6',
                'color': 'black'
            }
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
