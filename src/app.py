import pandas as pd
import dash
from dash import dcc, html, dash_table
import flask
from dash.dependencies import Input, Output

# Cargar datos
file_path = 'src/GRANDT_FINAL.csv'
df = pd.read_csv(file_path)

# Convertir columnas numéricas
numeric_cols = ["MINUTOS", "GOLES", "GOLES/90 HIST", "MINUTOS ULT 3", "GOLES ULT 3", "GOLES/90 ULT 3",
               "MINUTOS 2025", "GOLES 2025", "GOLES/90 2025"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Colores por posición
position_colors = {
    "ARQ": "#FFA07A",  # Anaranjado
    "DEF": "#FFD700",  # Amarillo
    "VOL": "#87CEFA",  # Celeste
    "DEL": "#FF6347"   # Rojo
}

# Inicializar aplicación Dash
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
])
server = app.server

# Estilos CSS mejorados
styles = {
    'header': {
        'background': 'linear-gradient(135deg, #1a7f3d 0%, #004d00 100%)',
        'color': 'white',
        'padding': '1.5rem',
        'textAlign': 'center',
        'marginBottom': '1.5rem',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    },
    'title': {
        'margin': '0',
        'fontSize': '2rem',
        'fontWeight': '700',
        'fontFamily': 'Roboto, sans-serif'
    },
    'subtitle': {
        'margin': '0.5rem 0 0',
        'fontSize': '1rem',
        'fontWeight': '300',
        'opacity': '0.9',
        'fontFamily': 'Roboto, sans-serif'
    },
    'filters-container': {
        'background': '#f5f5f5',
        'padding': '1rem',
        'borderRadius': '8px',
        'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
        'marginBottom': '1.5rem'
    },
    'filters-row': {
        'display': 'flex',
        'flexWrap': 'wrap',
        'gap': '15px',
        'justifyContent': 'center',
        'marginBottom': '0.8rem'
    },
    'filter-group': {
        'display': 'flex',
        'flexDirection': 'column',
        'minWidth': '200px',
        'flex': '1'
    },
    'filter-label': {
        'fontWeight': '500',
        'marginBottom': '6px',
        'color': '#444',
        'fontSize': '0.8rem'
    },
    'dropdown': {
        'width': '100%',
        'fontFamily': 'Roboto, sans-serif',
        'border': '1px solid #ddd',
        'borderRadius': '4px',
        'fontSize': '0.9rem'
    },
    'table-container': {
        'padding': '0 1rem',
        'marginBottom': '1.5rem',
        'width': '100%',
        'overflowX': 'auto'
    },
    'footer': {
        'textAlign': 'center',
        'padding': '1rem',
        'color': '#666',
        'fontSize': '0.8rem',
        'borderTop': '1px solid #e0e0e0',
        'marginTop': '1.5rem',
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
            # Primera fila de filtros (búsqueda y selección)
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
                        options=[{'label': team, 'value': team} for team in sorted(df['EQUIPO'].dropna().unique())],
                        multi=True,
                        placeholder="Todos los equipos...",
                        style=styles['dropdown']
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("BUSCAR JUGADOR", style=styles['filter-label']),
                    dcc.Input(
                        id='player-search',
                        type='text',
                        placeholder='Nombre del jugador...',
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
            ], style=styles['filters-row']),
            
            # Segunda fila de filtros (Goles/90)
            html.Div([
                html.Div([
                    html.Label("GOLES/90 HIST (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-hist-min',
                        type='number',
                        placeholder='Mínimo histórico...',
                        min=0,
                        step=0.1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("GOLES/90 ULT 3 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-ult3-min',
                        type='number',
                        placeholder='Mínimo últimos 3...',
                        min=0,
                        step=0.1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("GOLES/90 2025 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-2025-min',
                        type='number',
                        placeholder='Mínimo 2025...',
                        min=0,
                        step=0.1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
            ], style=styles['filters-row']),
            
            # Tercera fila de filtros (Minutos)
            html.Div([
                html.Div([
                    html.Label("MINUTOS HIST (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='minutos-hist-min',
                        type='number',
                        placeholder='Mínimo histórico...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("MINUTOS ULT 3 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='minutos-ult3-min',
                        type='number',
                        placeholder='Mínimo últimos 3...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("MINUTOS 2025 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='minutos-2025-min',
                        type='number',
                        placeholder='Mínimo 2025...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
            ], style=styles['filters-row']),
            
            # Cuarta fila de filtros (Goles totales)
            html.Div([
                html.Div([
                    html.Label("GOLES HIST (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-hist-total-min',
                        type='number',
                        placeholder='Mínimo histórico...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("GOLES ULT 3 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-ult3-total-min',
                        type='number',
                        placeholder='Mínimo últimos 3...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
                
                html.Div([
                    html.Label("GOLES 2025 (MÍNIMO)", style=styles['filter-label']),
                    dcc.Input(
                        id='goles-2025-total-min',
                        type='number',
                        placeholder='Mínimo 2025...',
                        min=0,
                        step=1,
                        style={**styles['dropdown'], 'padding': '6px', 'fontSize': '0.9rem'}
                    )
                ], style=styles['filter-group']),
            ], style=styles['filters-row']),
        ], style=styles['filters-container']),
    ]),
    
    html.Div([
        dash_table.DataTable(
            id='data-table',
            columns=[
                {'name': 'ID', 'id': 'ID'},
                {'name': 'Jugador', 'id': 'NOMBRE_JUGADOR'},
                {'name': 'Posición', 'id': 'POS'},
                {'name': 'Equipo', 'id': 'EQUIPO'},
                {'name': 'Min Hist', 'id': 'MINUTOS', 'type': 'numeric'},
                {'name': 'Goles Hist', 'id': 'GOLES', 'type': 'numeric'},
                {'name': 'G/90 Hist', 'id': 'GOLES/90 HIST', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'Min Ult3', 'id': 'MINUTOS ULT 3', 'type': 'numeric'},
                {'name': 'Goles Ult3', 'id': 'GOLES ULT 3', 'type': 'numeric'},
                {'name': 'G/90 Ult3', 'id': 'GOLES/90 ULT 3', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'Min 2025', 'id': 'MINUTOS 2025', 'type': 'numeric'},
                {'name': 'Goles 2025', 'id': 'GOLES 2025', 'type': 'numeric'},
                {'name': 'G/90 2025', 'id': 'GOLES/90 2025', 'type': 'numeric', 'format': {'specifier': '.2f'}}
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
                'padding': '10px',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_table={
                'minWidth': '100%',
                'overflowX': 'auto',
                'borderRadius': '8px',
                'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
                'border': '1px solid #e0e0e0',
                'fontFamily': 'Roboto, sans-serif'
            },
            style_data={
                'borderBottom': '1px solid #e0e0e0',
                'textAlign': 'center',
                'padding': '8px',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data_conditional=[
                # Colorear filas por posición
                *[
                    {
                        'if': {'column_id': 'POS', 'filter_query': f'{{POS}} = "{pos}"'},
                        'backgroundColor': color,
                        'color': '#333333',
                        'fontWeight': '500'
                    } for pos, color in position_colors.items()
                ],
                # Colorear celdas de Goles/90
                *[
                    {
                        'if': {'column_id': col, 'filter_query': f'{{{col}}} <= 0.1'},
                        'backgroundColor': '#f0f9e8'
                    } for col in ["GOLES/90 2025", "GOLES/90 HIST", "GOLES/90 ULT 3"]
                ],
                *[
                    {
                        'if': {'column_id': col, 'filter_query': f'{{{col}}} > 0.1 && {{{col}}} <= 0.2'},
                        'backgroundColor': '#ccebc5'
                    } for col in ["GOLES/90 2025", "GOLES/90 HIST", "GOLES/90 ULT 3"]
                ],
                *[
                    {
                        'if': {'column_id': col, 'filter_query': f'{{{col}}} > 0.2 && {{{col}}} <= 0.3'},
                        'backgroundColor': '#a8ddb5'
                    } for col in ["GOLES/90 2025", "GOLES/90 HIST", "GOLES/90 ULT 3"]
                ],
                *[
                    {
                        'if': {'column_id': col, 'filter_query': f'{{{col}}} > 0.3 && {{{col}}} <= 0.5'},
                        'backgroundColor': '#7bccc4'
                    } for col in ["GOLES/90 2025", "GOLES/90 HIST", "GOLES/90 ULT 3"]
                ],
                *[
                    {
                        'if': {'column_id': col, 'filter_query': f'{{{col}}} > 0.5 && {{{col}}} <= 0.7'},
                        'backgroundColor': '#43a2ca'
                    } for col in ["GOLES/90 2025", "GOLES/90 HIST", "GOLES/90 ULT 3"]
                ],
                *[
                    {
                        'if': {'column_id': col, 'filter_query': f'{{{col}}} > 0.7'},
                        'backgroundColor': '#0868ac',
                        'color': 'white'
                    } for col in ["GOLES/90 2025", "GOLES/90 HIST", "GOLES/90 ULT 3"]
                ]
            ],
            style_cell={
                'minWidth': '60px',
                'width': '80px',
                'maxWidth': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'fontSize': '0.8rem'
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
], style={
    'backgroundColor': '#f9f9f9', 
    'fontFamily': 'Roboto, sans-serif',
    'margin': '0',
    'padding': '0',
    'width': '100%',
    'minWidth': '1200px'
})

# Callbacks para filtros
@app.callback(
    Output('data-table', 'data'),
    [Input('position-filter', 'value'),
     Input('team-filter', 'value'),
     Input('player-search', 'value'),
     Input('goles-hist-min', 'value'),
     Input('goles-ult3-min', 'value'),
     Input('goles-2025-min', 'value'),
     Input('minutos-hist-min', 'value'),
     Input('minutos-ult3-min', 'value'),
     Input('minutos-2025-min', 'value'),
     Input('goles-hist-total-min', 'value'),
     Input('goles-ult3-total-min', 'value'),
     Input('goles-2025-total-min', 'value')]
)
def update_table(selected_positions, selected_teams, player_search, 
                 goles_hist_min, goles_ult3_min, goles_2025_min, 
                 minutos_hist_min, minutos_ult3_min, minutos_2025_min,
                 goles_hist_total_min, goles_ult3_total_min, goles_2025_total_min):
    filtered_df = df.copy()
    
    # Aplicar filtros
    if selected_positions:
        filtered_df = filtered_df[filtered_df['POS'].isin(
            [selected_positions] if isinstance(selected_positions, str) else selected_positions
        )]
    
    if selected_teams:
        filtered_df = filtered_df[filtered_df['EQUIPO'].isin(
            [selected_teams] if isinstance(selected_teams, str) else selected_teams
        )]
    
    if player_search:
        filtered_df = filtered_df[filtered_df['NOMBRE_JUGADOR'].str.contains(
            player_search, case=False, na=False
        )]
    
    # Filtros numéricos
    numeric_filters = {
        'GOLES/90 HIST': goles_hist_min,
        'GOLES/90 ULT 3': goles_ult3_min,
        'GOLES/90 2025': goles_2025_min,
        'MINUTOS': minutos_hist_min,
        'MINUTOS ULT 3': minutos_ult3_min,
        'MINUTOS 2025': minutos_2025_min,
        'GOLES': goles_hist_total_min,
        'GOLES ULT 3': goles_ult3_total_min,
        'GOLES 2025': goles_2025_total_min
    }
    
    for col, value in numeric_filters.items():
        if value is not None:
            filtered_df = filtered_df[filtered_df[col] >= float(value)]
    
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
