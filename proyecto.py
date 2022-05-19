from collections import defaultdict
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt
import networkx as nx
import time

start_time = time.time()
origin = input('Enter the origin coordinate of the path')
end = input('Enter the end coordinate of the path')

data = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
data['geometry'] = data['geometry'].apply(wkt.loads)
data = gpd.GeoDataFrame(data)

area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

data['harassmentRisk'].fillna(data['harassmentRisk'].mean(), inplace = True)

two_way = data.rename(columns ={'origin': 'destino','destination': 'origen' })
two_way = two_way[two_way['oneway'] == True]
two_way = two_way.rename(columns = {'destino': 'destination', 'origen': 'origin'})
two_way = two_way[['name', 'origin', 'destination', 'length', 'oneway', 'harassmentRisk',
       'geometry']]

two_way = two_way[['name', 'origin', 'destination', 'length', 'harassmentRisk',
       'geometry']]
data1 = data[['name', 'origin', 'destination', 'length', 'harassmentRisk',
       'geometry']]

dataframes = [data1, two_way]

streets = pd.concat(dataframes)
streets['weightedDist'] = streets['length'] * streets['harassmentRisk']



shortest = nx.from_pandas_edgelist(streets, source = 'origin', target = 'destination', edge_attr = 'weightedDist')
path_shortest = nx.dijkstra_path(shortest, source= origin, target = end, weight = True)
origins_shortest = path_shortest[:-1]
destinations_shortest = path_shortest[1:]

#Create plot
fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street data
data.plot(ax=ax, linewidth=1, edgecolor='dimgray')
length = 0
risk = 0
for i in range(len(origins_shortest)):
    dist = streets[(streets['origin'] == origins_shortest[i]) & (streets['destination'] == destinations_shortest[i])]
    dist.plot(ax = ax,linewidth=1, edgecolor='y')
    length += dist['length'].values
    risk += dist['harassmentRisk'].values
#recorrido.plot(ax=ax, linewidth=1, edgecolor='y')
exTime = time.time()-start_time
plt.title(f'Shortest Path \n Length: {int(length)} \n Risk: {int(risk)/len(origins_shortest)} \n Execution Time: {exTime}')
plt.tight_layout()
plt.show()


