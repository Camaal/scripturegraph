import json
import networkx as net
from itertools import combinations
from app import db
from app.models import References, Sources


# Low memory graph class
class ThinGraph(net.Graph):
    all_edge_dict = {"weight": 1}

    def single_edge_dict(self):
        return self.all_edge_dict

    edge_attr_dict_factory = single_edge_dict


# Create a network using source and target in references table
in_file = db.session.query(References.source, References.target).all()
g = net.Graph()

for edge in in_file:
    # Use the first and second value to define the edges
    g.add_edge(edge[0], edge[1])
    g.add_edge(edge[1], edge[0])


def getNeighborNetwork(verse):
    # Create a new network just for 01001001 and it's network of neighbors
    neighbor_net = net.Graph()

    # Get neighbor of source
    node_neighbors = [n for n in g.neighbors(verse)]

    # Get permutations of edges between neighbors
    perm = combinations(node_neighbors, 2)

    # Loop over each neighbor and add it to a new graph
    for n in g.neighbors(verse):
        neighbor_net.add_edge(verse, n)

    # Loop over each permutation as see if an edge exists in the original network, if so add it to the new one
    for i in list(perm):
        if g.has_edge(i[0], i[1]):
            neighbor_net.add_edge(i[0], i[1])
        elif g.has_edge(i[1], i[0]):
            neighbor_net.add_edge(i[1], i[0])
        else:
            pass

    # Get the degree for each node
    node_sizes = dict(neighbor_net.degree)

    # Set the position of each node using a Spring Layout
    pos = net.spring_layout(neighbor_net)

    # Set the node size
    node_size = {}
    for node in neighbor_net.nodes():
        for n in node_sizes:
            if n == node:
                node_size[node] = node_sizes[n] * 10

    # Init JSON
    data = {'nodes': [], 'edges': []}

    # Nodes
    for n in neighbor_net.nodes:
        node_name = db.session.query(Sources.bookName, Sources.chapter, Sources.verse, Sources.normDegree,
                                     Sources.redLetter) \
            .filter(Sources.id == n).first()

        if node_name[4] == "TRUE":
            ncolor = "rgba(183, 18, 27, .5)"
        else:
            ncolor = "rgba(0,0,0,.3)"

        # color = degreeColor(node_name[3])
        data['nodes'].append({
            "id": n,
            "label": str(node_name[0]) + " " + str(node_name[1]) + ":" + str(node_name[2]),
            "x": pos[n][0],
            "y": pos[n][1],
            "size": node_size[n] * 10,
            "color": ncolor
        })

    # Edges
    # ['line','curve','arrow','curvedArrow','dashed','dotted','parallel','tapered']

    for i, e in enumerate(neighbor_net.edges):
        data['edges'].append({
            "id": str(i),
            "source": str(e[0]),
            "target": str(e[1]),
            "size": 1,
            "type": "line",
            "edgeColor": 'default'
        })

    return json.dumps(data)
