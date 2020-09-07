import csv
import networkx as net
from itertools import permutations
import matplotlib.pyplot as plt

in_file = csv.reader(open('static/data/bible_study_edges.csv', 'r'), delimiter=',')

# Skip first row
next(in_file)

# Create a network
g = net.Graph()

for line in in_file:
    # Use the second and third columns to define the edges
    g.add_edge(line[0], line[1])

#Show the degree for each node
node_degree = [n for n in g.degree()]

source_scripture = '01001001'

#Create a new network just for 01001001 and it's network of neighbors
neighbor_net = net.Graph()

#Get neighbor of source
node_neighbors = [n for n in g.neighbors(source_scripture)]

#Get permutations of edges between neighbors
perm = permutations(node_neighbors, 2)

#Loop over each neighbor and add it to a new graph
for n in g.neighbors(source_scripture):
    neighbor_net.add_edge(source_scripture, n)


#Loop over each permutation as see if an edge exists in the original network, if so add it to the new one
for i in list(perm):
    if g.has_edge(i[0], i[1]):
        neighbor_net.add_edge(i[0], i[1])
    else:
        pass

net.draw(neighbor_net)
plt.show()


