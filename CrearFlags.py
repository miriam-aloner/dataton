import pandas as pd

# Ruta del archivo de datos
path = r'C:\Users\L01232389\PycharmProjects\PythonProject\PDN_S6\Excel\data.txt'

# Cargar el archivo .txt en un DataFrame (suponiendo que el archivo tiene un delimitador tabulador)
df = pd.read_csv(path, sep='\t')

# Verificar las primeras filas del DataFrame cargado
#print(df.head())

# Crear la variable 'count.planning' que contará las columnas relevantes para cada 'id'
df['count.planning'] = df[['planning.documents[0].documentType',
                           'planning.documents[0].title',
                           'planning.documents[0].description',
                           'planning.documents[0].url',
                           'planning.documents[0].datePublished',
                           'planning.documents[0].dateModified',
                           'planning.documents[1].format']].notnull().sum(axis=1)

# Crear la variable 'flag.planning' según la condición: si count.planning == 7, asignar 1, sino 0
df['flag.planning'] = df['count.planning'].apply(lambda x: 1 if x == 7 else 0)
# Verificar las nuevas columnas en el DataFrame
print(df[['id', 'state', 'count.planning', 'flag.planning']].head(2))
#__________________________________________________________________________________________________________

# Crear la variable 'count.tender' que contará las columnas relevantes para cada 'id'
df['count.tender'] = df[['tender.documents[0].documentType',
                         'tender.documents[0].title',
                         'tender.documents[0].description',
                         'tender.documents[0].url',
                         'tender.documents[0].datePublished',
                         'tender.documents[0].dateModified',
                         'tender.documents[0].format']].notnull().sum(axis=1)

# Crear la variable 'flag.tender' según la condición: si count.tender == 7, asignar 1, sino 0
df['flag.tender'] = df['count.tender'].apply(lambda x: 1 if x == 7 else 0)

# Verificar las nuevas columnas en el DataFrame
print(df[['id', 'state', 'count.tender', 'flag.tender']].head(2))

#__________________________________________________________________________________________________________
import numpy as np
# Convertir las fechas a formato datetime, especificando utc=True para manejar zonas horarias
df['tender.enquiryPeriod.startDate'] = pd.to_datetime(df['tender.enquiryPeriod.startDate'], errors='coerce', utc=True)
df['tender.enquiryPeriod.endDate'] = pd.to_datetime(df['tender.enquiryPeriod.endDate'], errors='coerce', utc=True)

# Verificar si la conversión fue exitosa
#print(df[['tender.enquiryPeriod.startDate', 'tender.enquiryPeriod.endDate']].head())

# Crear la variable 'date.tender' como la diferencia entre las fechas
df['date.tender'] = (df['tender.enquiryPeriod.startDate'] - df['tender.enquiryPeriod.endDate']).dt.days

# Crear la variable 'flagdate.tender' según la condición: si 'date.tender' es finito, asignar 1, sino 0
df['flagdate.tender'] = df['date.tender'].apply(lambda x: 1 if np.isfinite(x) else 0)

# Verificar las nuevas columnas en el DataFrame
print(df[['state', 'date.tender', 'flagdate.tender']].head(3))
print(df[['state', 'date.tender', 'flagdate.tender']].tail(3))
#_______________________________________________________________________________________________________

# Crear la variable 'resta.award' como la diferencia entre 'contracts[0].value.amount' y 'awards[0].value.amount'
df['resta.award'] = df['contracts[0].value.amount'] - df['awards[0].value.amount']

# Crear la variable 'porc.award' como la división entre 'resta.award' y 'awards[0].value.amount'
df['porc.award'] = df['resta.award'] / df['awards[0].value.amount']

# Crear la variable 'flag.award' según la condición: si 'porc.award' < 0.3, asignar 1, sino 0
df['flag.award'] = df['porc.award'].apply(lambda x: 1 if x < 0.3 else 0)

# Verificar las nuevas columnas en el DataFrame
print(df[['state', 'resta.award', 'porc.award', 'flag.award']].head(3))

# Contar cuántos valores '0' hay
#count_flag_award_0 = (df['flag.award'] == 0).sum()
#print(f"Hay {count_flag_award_0} valores '0'")

#________________________________________________________________________________________________________
# Agrupar por 'contracts[0].awardID' y sumar 'contracts[0].implementation.transactions[0].value.amount'
df['sumid.impletrans'] = df.groupby('contracts[0].awardID')['contracts[0].implementation.transactions[0].value.amount'].transform('sum')

# Calcular la diferencia entre 'sumid.impletrans' y 'contracts[0].value.amount' para 'resta.impletrans'
df['resta.impletrans'] = df['sumid.impletrans'] - df['contracts[0].value.amount']

# Crear la variable 'porc.impletrans' como la división entre 'resta.impletrans' y 'contracts[0].value.amount'
df['porc.impletrans'] = df['resta.impletrans'] / df['contracts[0].value.amount']

# Crear la variable 'flag.impletrans' según la condición: si 'porc.impletrans' > 0.05, asignar 'rojo=0', sino 'verde=1'
df['flag.impletrans'] = df['porc.impletrans'].apply(lambda x: 0 if x > 0.05 else 1)

# Verificar las nuevas columnas en el DataFrame
print(df[['id', 'sumid.impletrans', 'resta.impletrans', 'porc.impletrans', 'flag.impletrans']].head())

#____________________________________________________________________________________________________
# Agrupar por 'contracts[0].awardID' y mostrar los resultados
grouped = df.groupby('contracts[0].awardID')[['contracts[0].implementation.transactions[0].value.amount',
                                               'contracts[0].value.amount']].sum()

# Agregar las nuevas columnas 'sumid.impletrans', 'resta.impletrans', 'porc.impletrans' para los grupos
grouped['sumid.impletrans'] = grouped['contracts[0].implementation.transactions[0].value.amount']
grouped['resta.impletrans'] = grouped['sumid.impletrans'] - grouped['contracts[0].value.amount']
grouped['porc.impletrans'] = grouped['resta.impletrans'] / grouped['contracts[0].value.amount']

# Crear la variable 'flag.impletrans' para cada grupo
grouped['flag.impletrans'] = grouped['porc.impletrans'].apply(lambda x: 0 if x > 0.5 else 1)

# Mostrar los resultados por grupo de 'contracts[0].awardID'
#print(grouped)
#______________________________________________________________________________________
# Rutas para guardar los archivos CSV y Excel
output_df_csv_path = r'/PDN_S6/Excel/df_data.csv'
output_grouped_csv_path = r'C:\Users\L01232389\PycharmProjects\PythonProject\PDN_S6\grouped_data.csv'

# Guardar los DataFrames 'df' y 'grouped' en formato CSV
df.to_csv(output_df_csv_path, index=False)
grouped.to_csv(output_grouped_csv_path, index=False)

# Mensajes de confirmación
print(f"El archivo 'df' se ha guardado en: {output_df_csv_path}")
print(f"El archivo 'grouped' se ha guardado en: {output_grouped_csv_path}")
