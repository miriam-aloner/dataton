import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table


# Cargar el DataFrame (asegúrate de tener los datos correctamente cargados en 'df')
path = r'C:\Users\L01232389\PycharmProjects\PythonProject\PDN_S6\Excel\df_data.csv'
df = pd.read_csv(path)
#________________________________________________________________________________________________________
tabla_rename={'tender.id':'Número de licitación',
'tender.description': 'Descripción del proyecto',
"tender.procuringEntity.name": 'Nombre de Contratante',
"tender.value.amount": 'Valor del proyecto',
"tender.value.currency": 'Moneda',
"tender.procurementMethod": 'Tipo de licitación',
"tender.additionalProcurementCategories[0]": 'Categoría de mercado'}

df = df.rename(columns=tabla_rename)

columns_to_display = ["id",'Número de licitación','Descripción del proyecto','Nombre de Contratante','Valor del proyecto',
                      'Moneda','Tipo de licitación','Categoría de mercado']
# Definir las columnas a mostrar en la tabla
#columns_to_display = ["id","tender.id", "tender.description","tender.procuringEntity.name", "tender.value.amount","tender.value.currency", "tender.procurementMethod", "tender.additionalProcurementCategories[0]"]

# Filtrar las columnas en el DataFrame
filtered_df = df[columns_to_display]

#Definir el diccionario de renombrado grafico de barras
rename_dict = {
    'awards[0].title': 'Adjudicación',
    'planning.documents[0].title': 'Planeación',
    'tender.title': 'Licitación',
    'tender.documents[0].title': 'Aclaraciones',
    'contracts[0].title':'Contratación',
    }

# Renombrar las columnas
df = df.rename(columns=rename_dict)
#filtered_df = filtered_df.rename(columns=rename_dict)

# Especificar las columnas de interés con los nuevos nombres
columns_of_interest = ['Adjudicación', 'Planeación', 'Licitación', 'Aclaraciones', 'Contratación']

# Preparar datos de indicadores de 'flag' KPIS
df['flag.planning'] = df['flag.planning'].fillna(0)
df['flag.tender'] = df['flag.tender'].fillna(0)
df['flagdate.tender'] = df['flagdate.tender'].fillna(0)
df['flag.award'] = df['flag.award'].fillna(0)
df['flag.impletrans'] = df['flag.impletrans'].fillna(0)

# Preparar datos de gráfico de pay
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

#_________________________________________________________________


# Verificar que todas las columnas existen en el DataFrame
valid_columns = [col for col in columns_to_display if col in df.columns]

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([

    html.H1("CONOCE | Transparencia en Acción: Explorando las Contrataciones Públicas", style={'textAlign': 'left', 'color': 'white'}),

    # Filtros
    html.Div(
        style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px', 'color': 'black'},
        children=[
            dcc.Dropdown(
                id='filter-id',
                options=[{'label': str(id), 'value': str(id)} for id in df['id'].dropna().unique()],
                placeholder='Seleccionar ID',
                style={'width': '270px', 'margin-right': '10px'}
            ),
            dcc.Dropdown(
                id='filter-tender-id',
                options=[{'label': str(tid), 'value': str(tid)} for tid in df['Número de licitación'].dropna().unique()],
                placeholder='Seleccionar el Número de licitación',
                style={'width': '270px', 'margin-right': '10px'}
            ),
            dcc.Dropdown(
                id='filter-state',
                options=[{'label': state, 'value': state} for state in df['state'].dropna().unique()],
                placeholder='Seleccionar Estado',
                style={'width': '270px', 'margin-right': '10px'}
            ),
            dcc.Dropdown(
                id='filter-year',
                options=[{'label': year, 'value': year} for year in df['year'].dropna().unique()],
                placeholder='Seleccionar Año',
                style={'width': '270px'}
            )
        ]
    ),
    # Indicadores
    html.Div(
        style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px', 'color': 'white'},
        children=[
            html.Div([html.H4("Planeación", style={'textAlign': 'center'}), html.H2(id='indicator-planning', style={'textAlign': 'center'})]),
            html.Div([html.H4("Aclaraciones", style={'textAlign': 'center'}), html.H2(id='indicator-datetender', style={'textAlign': 'center'})]),
            html.Div([html.H4("Adjudicación", style={'textAlign': 'center'}), html.H2(id='indicator-tender', style={'textAlign': 'center'})]),
            html.Div([html.H4("Contratacón", style={'textAlign': 'center'}), html.H2(id='indicator-award', style={'textAlign': 'center'})]),
            html.Div([html.H4("Implementación", style={'textAlign': 'center'}), html.H2(id='indicator-impletrans', style={'textAlign': 'center'})]),
            ]
    ),

    # Gráficos
    html.Div([
        html.Div([dcc.Graph(id='mapa')], style={'width': '40%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='pie-chart')], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bar-chart')], style={'width': '30%', 'display': 'inline-block'})
        ,
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    # Tabla
    html.Div([dash_table.DataTable(
        id='table-data',
        columns=[{'name': col, 'id': col} for col in valid_columns],  # Usar las columnas válidas
        page_size=10,
        style_table={'height': '300px', 'overflowY': 'auto'},  # Scrollable table
        style_cell={'textAlign': 'center', 'color': 'black', 'backgroundColor': '#f1f1f1'},  # Estilo de las celdas
        style_header={'backgroundColor': 'gray', 'fontWeight': 'bold'},  # Estilo de encabezados
    ),
], style={'marginTop': '20px'})

], style = {'backgroundColor': '#1e1e1e', 'padding': '10px'})

# Callback para actualizar gráficos y tabla
@app.callback(
    [
        Output('filter-id', 'options'),
        Output('filter-tender-id', 'options'),
        Output('filter-state', 'options'),
        Output('filter-year', 'options'),
    ],
    [
        Input('filter-id', 'value'),
        Input('filter-tender-id', 'value'),
        Input('filter-state', 'value'),
        Input('filter-year', 'value')
    ]
)
def update_dashboard(selected_id, selected_tender_id, selected_state, selected_year):
    filtered_df = df.copy()

    if selected_id:
        filtered_df = filtered_df[filtered_df['id'].astype(str) == selected_id]
    if selected_year:
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
    if selected_tender_id:
        filtered_df = filtered_df[filtered_df['Número de licitación'].astype(str) == selected_tender_id]
    if selected_state:
        filtered_df = filtered_df[filtered_df['state'] == selected_state]

     # Generar opciones para cada dropdown basadas en los datos filtrados
    id_options = [{'label': str(id), 'value': str(id)} for id in filtered_df['id'].dropna().unique()]
    tender_id_options = [{'label': str(tid), 'value': str(tid)} for tid in filtered_df['Número de licitación'].dropna().unique()]
    state_options = [{'label': state, 'value': state} for state in filtered_df['state'].dropna().unique()]
    year_options = [{'label': year, 'value': year} for year in filtered_df['year'].dropna().unique()]

    return id_options, tender_id_options, state_options, year_options

# Callback para actualizar los gráficos, indicadores y la tabla
@app.callback(
    [
        Output('bar-chart', 'figure'),
        Output('pie-chart', 'figure'),
        Output('mapa', 'figure'),
        Output('indicator-planning', 'children'),
        Output('indicator-datetender', 'children'),
        Output('indicator-tender', 'children'),
        Output('indicator-award', 'children'),
        Output('indicator-impletrans', 'children'),
        Output('table-data', 'data')
    ],
    [
        Input('filter-id', 'value'),
        Input('filter-tender-id', 'value'),
        Input('filter-state', 'value'),
        Input('filter-year', 'value')
    ]
)
def update_graphs_and_indicators(selected_id, selected_tender_id, selected_state, selected_year):
    filtered_df = df.copy()

    # Aplicar filtros
    if selected_id:
        filtered_df = filtered_df[filtered_df['id'].astype(str) == selected_id]
    if selected_tender_id:
        filtered_df = filtered_df[filtered_df['Número de licitación'].astype(str) == selected_tender_id]
    if selected_state:
        filtered_df = filtered_df[filtered_df['state'] == selected_state]
    if selected_year:
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]

    # Verificar si el DataFrame filtrado tiene datos
    if filtered_df.empty:
        # Si no hay datos, se retornan gráficos vacíos y datos vacíos para la tabla
        return {}, {}, {}, None, None, None, None, None, []

    # Indicadores con lógica ajustada
    def calculate_indicator(flag_column):
        unique_values = filtered_df[flag_column].unique()
        if len(unique_values) == 1:  # Si solo hay un valor único
            value = unique_values[0]
            if value == 1:
                return "✅"
            elif value == 0:
                return "❌"
        # Si hay más de un valor o el valor único no es 0 ni 1, devolvemos la suma
        return filtered_df[flag_column].sum()

    planning_sum = calculate_indicator('flag.planning')
    tender_sum = calculate_indicator('flag.tender')
    tenderdate_sum = calculate_indicator('flagdate.tender')
    award_sum = calculate_indicator('flag.award')
    impletrans_sum = calculate_indicator('flag.impletrans')

    # Gráficos
    frequency_counts = filtered_df[columns_of_interest].notna().sum()
    frequency_table = frequency_counts.reset_index(name='count')
    frequency_table.columns = ['Variable', 'Count']
    bar_chart_updated = px.bar(frequency_table, x='Variable', y='Count', title="Conteo de valores no nulos",template="plotly_dark")
    year_count_df = filtered_df.groupby('year').size().reset_index(name='count')
    pie_chart_updated = px.pie(year_count_df, names='year', values='count', title="Distribución de Tickets por Año",template="plotly_dark")

    count_df = filtered_df.groupby(['state', 'latitud', 'longitud']).size().reset_index(name='count')
    map_updated = px.scatter_geo(
        count_df,
        lat='latitud',
        lon='longitud',
        size='count',
        color='count',  # Utilizar valores continuos para el color
        color_continuous_scale=["#4b0082", "#9370db", "#d3d3d3"],  # Gradiente de morado a gris
        hover_name='state',
        hover_data=['count'],
        projection="mercator",
        title="Distribución por Estado",
        template="plotly_dark"
    )

    # Gráfico de Barras
    bar_chart_updated = px.bar(
        frequency_table,
        x='Variable',
        y='Count',
        title="Conteo de valores no nulos",
        template="plotly_dark",
        color='Variable',
        color_discrete_sequence=["#9370db"]
    )

    # Gráfico de Pastel
    pie_chart_updated = px.pie(
        year_count_df,
        names='year',
        values='count',
        title="Distribución de Tickets por Año",
        template="plotly_dark",
        color_discrete_sequence=["#9370db", "#4b0082", "#d3d3d3", "#6a0dad", "#a9a9a9"]  # Morado y gris
    )

    # Configuración de las líneas y los límites
    map_updated.update_geos(
        projection_type="mercator",
        lonaxis=dict(range=[-118, -86]),
        lataxis=dict(range=[14, 33]),
        showcoastlines=True,
        coastlinecolor="white",
        showland=True,
        landcolor="rgb(50, 50, 50)",
        showcountries=True,
        countrycolor="white",
        showsubunits=True,
        subunitcolor='white',
        showframe=True,
        fitbounds="locations"
    )

    # Personalización del tooltip y desactivación de la leyenda
    map_updated.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Count: %{marker.size}<extra></extra>",
    )

    # Tabla
    table_data = filtered_df[valid_columns].to_dict('records')  # Usar las columnas válidas

    return bar_chart_updated, pie_chart_updated, map_updated, planning_sum, tenderdate_sum, tender_sum, award_sum, impletrans_sum, table_data


if __name__ == '__main__':
    app.run_server(debug=True)