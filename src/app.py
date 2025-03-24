import pandas as pd
import dash
from dash import dcc, html, dash_table
import flask
from dash.dependencies import Input, Output

# Cargar datos
file_path = 'GRANDT_FINAL.csv'
df = pd.read_csv(file_path)

# Asegurar que los nombres de columnas sean correctos
df.columns = ["Equipo", "Jugador", "Posición", "Link", "Minutos", "Goles", "Goles/90 Hist", "Minutos 2025", "Goles 2025", "Goles/90 2025"]

# Convertir columnas numéricas, reemplazando valores no numéricos con NaN
numeric_cols = ["Minutos", "Goles", "Goles/90 Hist", "Minutos 2025", "Goles 2025", "Goles/90 2025"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Reemplazar NaN con 0 o algún valor por defecto si es necesario
df.fillna(0, inplace=True)

# Colores por posición
position_colors = {
    "ARQ": "#FFA07A",  # Anaranjado
    "DEF": "#FFD700",  # Amarillo
    "VOL": "#87CEFA",  # Celeste
    "DEL": "#FF6347"   # Rojo
}

# Inicializar aplicación Dash con external stylesheets
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
]

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
server = app.server

# Definir estilos CSS
styles = {
    'header': {
        'background': 'linear-gradient(135deg, #1a7f3d 0%, #004d00 100%)',
        'color': 'white',
        'padding': '2rem',
        'textAlign': 'center',
        'marginBottom': '2rem',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    },
    'title': {
        'margin': '0',
        'fontSize': '2.5rem',
        'fontWeight': '700',
        'fontFamily': 'Roboto, sans-serif'
    },
    'subtitle': {
        'margin': '0.5rem 0 0',
        'fontSize': '1.2rem',
        'fontWeight': '300',
        'opacity': '0.9',
        'fontFamily': 'Roboto, sans-serif'
    },
    'filters-container': {
        'background': '#f5f5f5',
        'padding': '1.5rem',
        'borderRadius': '8px',
        'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
        'marginBottom': '2rem'
    },
    'filters-row': {
        'display': 'flex',
        'flexWrap': 'wrap',
        'gap': '20px',
        'justifyContent': 'center',
        'marginBottom': '1rem'
    },
    'filter-group': {
        'display': 'flex',
        'flexDirection': 'column',
        'minWidth': '250px'
    },
    'filter-label': {
        'fontWeight': '500',
        'marginBottom': '8px',
        'color': '#444',
        'fontSize': '0.9rem'
    },
    'dropdown': {
        'width': '100%',
        'fontFamily': 'Roboto, sans-serif',
        'border': '1px solid #ddd',
        'borderRadius': '4px'
    },
    'table-container': {
        'padding': '0 2rem',
        'marginBottom': '2rem'
    },
    'footer': {
        'textAlign': 'center',
        'padding': '1.5rem',
        'color': '#666',
        'fontSize': '0.9rem',
        'borderTop': '1px solid #e0e0e0',
        'marginTop': '2rem',
        'fontFamily': 'Roboto, sans-serif'
    }
}

app.layout = html.Div([
    html.Div([
        html.H1("GRANDT PROMIEDOS", style=styles['title']),
        html.P("Estadísticas detalladas de jugadores - Temporada 2025", style=styles['subtitle']),
    ], style=styles['header']),
    
    html.Div([
        html.Div([
            # Filtros por posición y equipo
            html.Div([
                html.Div([
                    html.Label("FILTRAR POR POSICIÓN", style=styles['filter-label']),
                    dcc.Dropdown(
                        id='position-filter',
                        options=[{'label': pos, 'value': pos} for pos in position_colors.keys()],
                        multi=True,
                        placeholder="Todas las posiciones...",
                        style=styles['dropdown']
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("FILTRAR POR EQUIPO", style=styles['filter-label']),
                    dcc.Dropdown(
                        id='team-filter',
                        options=[{'label': team, 'value': team} for team in sorted(df['Equipo'].unique())],
                        multi=True,
                        placeholder="Todos los equipos...",
                        style=styles['dropdown']
                    )
                ], style=styles['filter-group']),
                
                # Buscador por nombre de jugador
                html.Div([
                    html.Label("BUSCAR JUGADOR", style=styles['filter-label']),
                    dcc.Input(
                        id='player-search',
                        type='text',
                        placeholder='Nombre del jugador...',
                        style={**styles['dropdown'], 'padding': '8px'}
                    )
                ], style=styles['filter-group']),
            ], style=styles['filters-row']),
            
            # Segunda fila de filtros (numéricos)
            html.Div([
                html.Div([
                    html.Label("GOLES/90 HIST (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-hist-min',
                        type='number',
                        placeholder='Mínimo...',
                        min=0,
                        step=0.1,
                        style={**styles['dropdown'], 'padding': '8px'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("GOLES/90 2025 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-2025-min',
                        type='number',
                        placeholder='Mínimo...',
                        min=0,
                        step=0.1,
                        style={**styles['dropdown'], 'padding': '8px'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("MINUTOS HIST (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='minutos-hist-min',
                        type='number',
                        placeholder='Mínimo...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '8px'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("MINUTOS 2025 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='minutos-2025-min',
                        type='number',
                        placeholder='Mínimo...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '8px'}
                    )
                ], style=styles['filter-group']),
            ], style=styles['filters-row']),
        ], style=styles['filters-container']),
    ]),
    
    html.Div([
        dash_table.DataTable(
            id='data-table',
            columns=[
                {'name': col, 'id': col, 'deletable': False, 'selectable': True, 
                 'type': 'numeric' if "Minutos" in col or "Goles" in col else 'text',
                 'format': {'specifier': '.2f'} if 'Goles/90' in col else None}
                for col in df.columns if col != "Link"
            ],
            data=df.to_dict('records'),
            filter_action='none',
            sort_action='native',
            sort_mode='multi',
            page_action='native',
            page_size=20,
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold',
                'fontFamily': 'Roboto, sans-serif',
                'textAlign': 'center',
                'border': 'none',
                'padding': '12px'
            },
            style_table={
                'overflowX': 'auto',
                'borderRadius': '8px',
                'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
                'border': '1px solid #e0e0e0',
                'fontFamily': 'Roboto, sans-serif'
            },
            style_data={
                'borderBottom': '1px solid #e0e0e0',
                'textAlign': 'center',
                'padding': '12px'
            },
            style_data_conditional=[
                # Colorear filas por posición
                *[
                    {
                        'if': {'filter_query': '{{Posición}} = "{}"'.format(pos), 'column_id': col},
                        'backgroundColor': color,
                        'color': '#333333',
                        'fontWeight': '500'
                    } for pos, color in position_colors.items() for col in df.columns if col not in ["Goles/90 2025", "Goles/90 Hist", "Link"]
                ],
                # Colorear celdas de Goles/90 con gradiente
                {
                    'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} <= 0.1'},
                    'backgroundColor': '#f0f9e8'
                },
                {
                    'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} > 0.1 && {Goles/90 2025} <= 0.2'},
                    'backgroundColor': '#ccebc5'
                },
                {
                    'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} > 0.2 && {Goles/90 2025} <= 0.3'},
                    'backgroundColor': '#a8ddb5'
                },
                {
                    'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} > 0.3 && {Goles/90 2025} <= 0.5'},
                    'backgroundColor': '#7bccc4'
                },
                {
                    'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} > 0.5 && {Goles/90 2025} <= 0.7'},
                    'backgroundColor': '#43a2ca'
                },
                {
                    'if': {'column_id': 'Goles/90 2025', 'filter_query': '{Goles/90 2025} > 0.7'},
                    'backgroundColor': '#0868ac',
                    'color': 'white'
                },
                # Mismo gradiente para Goles/90 Hist
                {
                    'if': {'column_id': 'Goles/90 Hist', 'filter_query': '{Goles/90 Hist} <= 0.1'},
                    'backgroundColor': '#f0f9e8'
                },
                {
                    'if': {'column_id': 'Goles/90 Hist', 'filter_query': '{Goles/90 Hist} > 0.1 && {Goles/90 Hist} <= 0.2'},
                    'backgroundColor': '#ccebc5'
                },
                {
                    'if': {'column_id': 'Goles/90 Hist', 'filter_query': '{Goles/90 Hist} > 0.2 && {Goles/90 Hist} <= 0.3'},
                    'backgroundColor': '#a8ddb5'
                },
                {
                    'if': {'column_id': 'Goles/90 Hist', 'filter_query': '{Goles/90 Hist} > 0.3 && {Goles/90 Hist} <= 0.5'},
                    'backgroundColor': '#7bccc4'
                },
                {
                    'if': {'column_id': 'Goles/90 Hist', 'filter_query': '{Goles/90 Hist} > 0.5 && {Goles/90 Hist} <= 0.7'},
                    'backgroundColor': '#43a2ca'
                },
                {
                    'if': {'column_id': 'Goles/90 Hist', 'filter_query': '{Goles/90 Hist} > 0.7'},
                    'backgroundColor': '#0868ac',
                    'color': 'white'
                }
            ],
            style_cell={
                'minWidth': '80px', 'width': '100px', 'maxWidth': '180px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_as_list_view=True,
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
        )
    ], style=styles['table-container']),
    
    html.Div([
        html.P("© 2025 GRANDT PROMIEDOS - Todos los derechos reservados", style=styles['footer'])
    ])
], style={'backgroundColor': '#f9f9f9', 'fontFamily': 'Roboto, sans-serif'})

# Callbacks para filtros
@app.callback(
    Output('data-table', 'data'),
    [Input('position-filter', 'value'),
     Input('team-filter', 'value'),
     Input('player-search', 'value'),
     Input('goles-hist-min', 'value'),
     Input('goles-2025-min', 'value'),
     Input('minutos-hist-min', 'value'),
     Input('minutos-2025-min', 'value')]
)
def update_table(selected_positions, selected_teams, player_search, 
                 goles_hist_min, goles_2025_min, minutos_hist_min, minutos_2025_min):
    filtered_df = df.copy()
    
    # Aplicar filtros uno por uno
    if selected_positions:
        filtered_df = filtered_df[filtered_df['Posición'].isin(selected_positions)]
    
    if selected_teams:
        filtered_df = filtered_df[filtered_df['Equipo'].isin(selected_teams)]
    
    if player_search:
        filtered_df = filtered_df[filtered_df['Jugador'].str.contains(player_search, case=False)]
    
    if goles_hist_min is not None:
        filtered_df = filtered_df[filtered_df['Goles/90 Hist'] >= goles_hist_min]
    
    if goles_2025_min is not None:
        filtered_df = filtered_df[filtered_df['Goles/90 2025'] >= goles_2025_min]
    
    if minutos_hist_min is not None:
        filtered_df = filtered_df[filtered_df['Minutos'] >= minutos_hist_min]
    
    if minutos_2025_min is not None:
        filtered_df = filtered_df[filtered_df['Minutos 2025'] >= minutos_2025_min]
    
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
