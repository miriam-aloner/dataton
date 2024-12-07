import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Cargar el DataFrame (asegúrate de tener los datos correctamente cargados en 'df')
path =r'C:\Users\L01232389\PycharmProjects\PythonProject\PDN_S6\df_data.csv'
df = pd.read_csv(path)

# Verificar si las columnas 'latitud', 'longitud', y 'state' existen
df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')

# Agrupar los datos por 'state' y 'id' para contar el número de ocurrencias
count_df = df.groupby(['state', 'latitud', 'longitud']).size().reset_index(name='count')

# Crear el mapa con Plotly, donde el color y el tamaño dependen del 'count'
fig = px.scatter_geo(count_df,
                     lat='latitud',
                     lon='longitud',
                     size='count',  # Tamaño de las burbujas según el conteo
                     color='count',  # Colorear las burbujas según el conteo
                     hover_name='state',
                     hover_data=['count'],
                     projection="mercator",  # Usar Mercator como proyección
                     title="DATATON AS14",  # Título del mapa
                     color_continuous_scale='Viridis',  # Usar un degradado de colores
                     size_max=40,  # Tamaño máximo de las burbujas
                     opacity=0.6,  # Opacidad de las burbujas
                     scope="north america",  # Limitar a América del Norte (incluye México)
                     template="plotly_dark")  # Usar un tema oscuro para mejor visualización

# Ajustar el mapa para centrarse en México (establecer los límites de latitud y longitud)
fig.update_geos(
    projection_type="mercator",
    lonaxis=dict(range=[-118, -86]),  # Rango de longitudes para México
    lataxis=dict(range=[14, 33])  # Rango de latitudes para México
)

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Crear el layout del dashboard
app.layout = html.Div([
    html.H1("DATATON AS14"),  # Título del dashboard

    # Mapa interactivo
    dcc.Graph(
        id='mapa',
        figure=fig
    ),
])

# Ejecutar el servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True)
