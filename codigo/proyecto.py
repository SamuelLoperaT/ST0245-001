from collections import defaultdict
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt

data = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')

data['harassmentRisk'].fillna(data['harassmentRisk'].mean(), inplace = True)

doble_sentido = data.rename(columns ={'origin': 'destino','destination': 'origen' })
doble_sentido = doble_sentido[doble_sentido['oneway'] == True]
doble_sentido = doble_sentido.rename(columns = {'destino': 'destination', 'origen': 'origin'})
doble_sentido = doble_sentido[['name', 'origin', 'destination', 'length', 'oneway', 'harassmentRisk',
       'geometry']]

doble_sentido = doble_sentido[['name', 'origin', 'destination', 'length', 'harassmentRisk',
       'geometry']]
data1 = data[['name', 'origin', 'destination', 'length', 'harassmentRisk',
       'geometry']]

dataframes = [data1, doble_sentido]

calles = pd.concat(dataframes)

hash_table = defaultdict(list)
for ind in calles.index:
    hash_table[data['origin'][ind]].append((data['destination'][ind], data['length'][ind], data['harassmentRisk'][ind]))

