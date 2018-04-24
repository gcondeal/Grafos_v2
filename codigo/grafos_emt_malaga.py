import requests
import codecs
import json
import networkx as nx
from networkx.algorithms import community
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import operator


#consulta para descargar las paradas
response = requests.get("http://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasYParadas/lineasyparadas.geojson")
paradas = response.content.decode('utf-8-sig')

paradasJson = json.loads(paradas)

#guardamos en disco el fichero descargado
f = open('data/paradas_emt.json', 'w', encoding='utf-8', newline='') #codecs.open('data/paradas_emt.json', 'w')
f.write(paradas)

g = nx.DiGraph()

# vamos preparando la lista de nodos y sus relaciones
for paradasPorLinea in paradasJson:
    paradaOrigen = None
    paradaDestino = None
    for paradaDeLinea in paradasPorLinea['paradas']:
        if paradaOrigen == None:
            paradaOrigen = paradaDeLinea['parada']
            g.add_node(paradaOrigen['codParada'],linea=paradasPorLinea['codLinea'],name=paradaOrigen['nombreParada'],latitud=paradaOrigen['latitud'], longitud=paradaOrigen['longitud'])
        else:
            paradaDestino = paradaDeLinea['parada']
            g.add_node(paradaDestino['codParada'],linea=paradasPorLinea['codLinea'],name=paradaDestino['nombreParada'],latitud=paradaDestino['latitud'], longitud=paradaDestino['longitud'])

        if paradaOrigen != None and paradaDestino != None:
            # Adds edges from a list
            g.add_edges_from([(paradaOrigen['codParada'], paradaDestino['codParada'])])
            paradaOrigen = paradaDestino

# layout = nx.spring_layout(g)
# nx.draw_networkx_nodes(g, layout, node_size=100, node_color='blue', alpha=0.3)
# nx.draw_networkx_edges(g, layout)
# nx.draw_networkx_labels(g, layout, font_size=8, font_family='sans-serif')
# plt.show()


print("\nMEDIDAS DEL GRAFO")
print("\tNº nodes: ", g.number_of_nodes())
print("\tNº edges: ", g.number_of_edges())
print("\tIs directed: ", g.is_directed())

print("\tIs strongly connected: ", nx.is_strongly_connected(g))
print("\tIs weakly connected: ", nx.is_weakly_connected(g))
print("\tNº weakly connected nodes: ", nx.number_weakly_connected_components(g))


degreeCent = nx.degree_centrality(g)
closeness = nx.closeness_centrality(g)
betweenness = nx.betweenness_centrality(g)
pagerank = nx.pagerank(g)
print('\tDegree:', degreeCent)
print('\tMAX DEG: ', max(degreeCent.items(), key=operator.itemgetter(1)))
print('\tCloseness:', closeness)
print('\tMAX CLOSENESS: ', max(closeness.items(), key=operator.itemgetter(1)))
print('\tBetweenness:', betweenness)
print('\tMAX BETWEENNESS: ', max(betweenness.items(), key=operator.itemgetter(1)))
print('\tPageRank:', pagerank)
print('\tMAX PAGERANK: ', max(pagerank.items(), key=operator.itemgetter(1)))



g_json = json_graph.node_link_data(g)
with open('data/graph_json.txt', 'w') as f:
    print(json.dump(g_json, f, indent=1))