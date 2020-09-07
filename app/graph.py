import csv
import networkx as net

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

#Show neighbor of node
node_neighbors = [n for n in g.neighbors('01001001')]
print(node_neighbors)

#Loop over each neighbor node and see if it's connected to any of the other neighbors

#Create a new network just for 01001001 and it's network of nieghbors


