from collections import defaultdict
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt
import networkx as nx

origin = input('Enter the origin coordinate of the path')
end = input('Enter the end coordinate of the path')

data = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
data['geometry'] = data['geometry'].apply(wkt.loads)
data = gpd.GeoDataFrame(data)

area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

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



corto = nx.from_pandas_edgelist(calles, source = 'origin', target = 'destination', edge_attr = 'length')
recorrido_dist = nx.dijkstra_path(corto, source= origin, target = end, weight = True)
origenes_dist = recorrido_dist[:-1]
destinos_dist = recorrido_dist[1:]

acoso = nx.from_pandas_edgelist(calles, source = 'origin', target = 'destination', edge_attr = 'harassmentRisk')
recorrido_risk = nx.dijkstra_path(acoso, source= origin, target = end, weight = True)
origenes_risk = recorrido_risk[:-1]
destinos_risk = recorrido_risk[1:]

#Create plot
fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street data
data.plot(ax=ax, linewidth=1, edgecolor='dimgray')
for i in range(len(origenes_dist)):
    dist = calles[(calles['origin'] == origenes_dist[i]) & (calles['destination'] == destinos_dist[i])]
    dist.plot(ax = ax,linewidth=1, edgecolor='y')
#recorrido.plot(ax=ax, linewidth=1, edgecolor='y')
plt.title(' Shortest Path')
plt.tight_layout()
plt.show()

#Create plot
fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street data
data.plot(ax=ax, linewidth=1, edgecolor='dimgray')
for i in range(len(origenes_risk)):
    risk = calles[(calles['origin'] == origenes_risk[i]) & (calles['destination'] == destinos_risk[i])]
    risk.plot(ax = ax,linewidth=1, edgecolor='y')
#recorrido.plot(ax=ax, linewidth=1, edgecolor='y')
plt.title('Least Harassment Risk Path')
plt.tight_layout()
plt.show()
