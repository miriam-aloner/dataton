import pandas as pd

# Diccionario de coordenadas por estado
coordinates = {
    'Aguascalientes': {'latitud': 21.885256, 'longitud': -102.291567},
    'Baja California': {'latitud': 32.653752, 'longitud': -115.468926},
    'Baja California Sur': {'latitud': 24.142635, 'longitud': -110.310921},
    'Campeche': {'latitud': 19.830125, 'longitud': -90.53491},
    'Chiapas': {'latitud': 16.756931, 'longitud': -93.129235},
    'Chihuahua': {'latitud': 28.63528, 'longitud': -106.08889},
    'Ciudad de México': {'latitud': 19.432608, 'longitud': -99.133209},
    'Coahuila': {'latitud': 27.058675, 'longitud': -101.706829},
    'Colima': {'latitud': 19.245234, 'longitud': -103.724711},
    'Durango': {'latitud': 24.02772, 'longitud': -104.653175},
    'Guanajuato': {'latitud': 21.019015, 'longitud': -101.257358},
    'Guerrero': {'latitud': 17.439192, 'longitud': -99.545097},
    'Hidalgo': {'latitud': 20.091096, 'longitud': -98.762387},
    'Jalisco': {'latitud': 20.659698, 'longitud': -103.349609},
    'Estado de México': {'latitud': 19.357374, 'longitud': -99.688155},
    'Michoacán': {'latitud': 19.56652, 'longitud': -101.706829},
    'Morelos': {'latitud': 18.681304, 'longitud': -99.101349},
    'Nayarit': {'latitud': 21.751384, 'longitud': -104.845461},
    'Nuevo León': {'latitud': 25.686614, 'longitud': -100.316113},
    'Oaxaca': {'latitud': 17.059417, 'longitud': -96.721621},
    'Puebla': {'latitud': 19.041296, 'longitud': -98.2062},
    'Querétaro': {'latitud': 20.588793, 'longitud': -100.389888},
    'Quintana Roo': {'latitud': 19.181739, 'longitud': -88.479137},
    'San Luis Potosí': {'latitud': 22.156469, 'longitud': -100.98554},
    'Sinaloa': {'latitud': 24.798401, 'longitud': -107.389722},
    'Sonora': {'latitud': 29.072967, 'longitud': -110.955919},
    'Tabasco': {'latitud': 17.840917, 'longitud': -92.618927},
    'Tamaulipas': {'latitud': 23.736916, 'longitud': -99.141116},
    'Tlaxcala': {'latitud': 19.318162, 'longitud': -98.237378},
    'Veracruz': {'latitud': 19.173773, 'longitud': -96.134224},
    'Yucatán': {'latitud': 20.709878, 'longitud': -89.094337},
    'Zacatecas': {'latitud': 22.770924, 'longitud': -102.583253}
}

# Crear un DataFrame de estados y sus coordenadas
states_df = pd.DataFrame.from_dict(coordinates, orient='index').reset_index()
states_df.columns = ['state', 'latitud', 'longitud']
states_df['coordenada'] = states_df.apply(lambda row: f"({row['latitud']}, {row['longitud']})", axis=1)

print(states_df.head(1))
#_______________________________________________________________________________________________________

import os
import pandas as pd
import json
from glob import glob

# Ruta a la carpeta que contiene los archivos JSON
json_file_path = r'C:\Users\L01232389\PycharmProjects\PythonProject\PDN_S6'

# Obtener la lista de todos los archivos JSON en la carpeta
json_files = glob(os.path.join(json_file_path, '*.json'))

# Lista para almacenar los datos procesados
all_data = []

# Función recursiva para aplanar listas y diccionarios
def flatten_json(nested_json, parent_key=''):
    """Aplana un JSON anidado."""
    items = []
    for key, value in nested_json.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key).items())
        elif isinstance(value, list):
            # Expandir listas, aplanar cada elemento y numerarlo
            for i, item in enumerate(value):
                if isinstance(item, (dict, list)):
                    items.extend(flatten_json(item, f"{new_key}[{i}]").items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, value))
    return dict(items)

# Iterar sobre todos los archivos JSON y procesarlos
for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as file:  # Especificar 'utf-8' para evitar problemas de codificación
        data = json.load(file)

    # Aplanar los datos del archivo JSON
    flattened_data = [flatten_json(record) for record in data]

    # Agregar los datos a la lista total
    for record in flattened_data:
        # Agregar el nombre del archivo como 'source_file'
        record['source_file'] = os.path.basename(json_file)  # Usar el nombre del archivo sin la ruta completa
    all_data.extend(flattened_data)

# Convertir el resultado a un DataFrame
df = pd.DataFrame(all_data)

# Imprimir las primeras filas
print(df.head(1))

# Función para extraer el nombre del estado desde el nombre del archivo
def extract_state(filename):
    return filename.split('_')[0]  # Extraer la parte antes del primer "_"

# Agregar una nueva columna 'state' al DataFrame usando 'source_file'
df['state'] = df['source_file'].apply(lambda x: extract_state(x))

# Mostrar el DataFrame actualizado
print(df.tail(1))

# Imprimir las columnas únicas del DataFrame
#print(df.columns.unique().tolist())

#_________________________________________________________________________________________________________
# Lista de las columnas que deseas filtrar
columns_to_keep = [
    'awards[0].contractPeriod.endDate', 'awards[0].contractPeriod.startDate',
    'awards[0].description', 'awards[0].id', 'awards[0].status',
    'awards[0].suppliers[0].id', 'awards[0].suppliers[0].name',
    'awards[0].title', 'awards[0].value.amount', 'awards[0].value.currency',
    'contracts[0].awardID', 'contracts[0].description', 'contracts[0].id',
    'contracts[0].implementation.transactions[0].date',
    'contracts[0].implementation.transactions[0].id',
    'contracts[0].implementation.transactions[0].payee.id',
    'contracts[0].implementation.transactions[0].payee.name',
    'contracts[0].implementation.transactions[0].payer.id',
    'contracts[0].implementation.transactions[0].payer.name',
    'contracts[0].implementation.transactions[0].value.amount',
    'contracts[0].implementation.transactions[0].value.currency',
    'contracts[0].period.endDate', 'contracts[0].period.startDate',
    'contracts[0].status', 'contracts[0].title', 'contracts[0].value.amount',
    'date', 'id', 'initiationType',
    'planning.documents[0].dateModified', 'planning.documents[0].datePublished',
    'planning.documents[0].description', 'planning.documents[0].documentType',
    'planning.documents[0].title', 'planning.documents[0].url',
    'planning.documents[1].format', 'tag[0]', 'tender.additionalProcurementCategories[0]',
    'tender.awardCriteria', 'tender.awardCriteriaDetails', 'tender.description',
    'tender.documents[0].dateModified', 'tender.documents[0].datePublished',
    'tender.documents[0].description', 'tender.documents[0].documentType',
    'tender.documents[0].format', 'tender.documents[0].title', 'tender.documents[0].url',
    'tender.enquiryPeriod.endDate', 'tender.enquiryPeriod.startDate', 'tender.id',
    'tender.mainProcurementCategory', 'tender.minValue.amount',
    'tender.minValue.currency', 'tender.procurementMethod',
    'tender.procurementMethodDetails', 'tender.procurementMethodRationale',
    'tender.procuringEntity.id', 'tender.procuringEntity.name',
    'tender.status', 'tender.title', 'tender.value.amount', 'tender.value.currency',
    'state'  # Suponiendo que 'state' es una columna ya añadida
]
# Filtrar el DataFrame para incluir solo las columnas seleccionadas
filtered_df = df[columns_to_keep]

# Mostrar las primeras filas del DataFrame filtrado
#print(filtered_df.head(1))
#print(filtered_df.columns.unique().tolist())

#_______________________________________________________________________________________________________

# Hacemos un merge entre filtered_df y states_df usando la columna 'state'
merged_df = pd.merge(filtered_df, states_df[['state', 'latitud', 'longitud', 'coordenada']],
                     on='state', how='left')

# Mostrar las primeras filas del DataFrame resultante
print(merged_df.head(1))

#_________________________________________________________________________________________________________

# Especificar la ruta completa para guardar el archivo
output_file_path = r'/PDN_S6/Excel/data.txt'

# Guardar el DataFrame en un archivo .txt con delimitador tabulador
merged_df.to_csv(output_file_path, sep='\t', index=False)

# Confirmar que el archivo se ha guardado correctamente
print(f"El DataFrame se ha guardado en: {output_file_path}")
