import json
import networkx as net
from itertools import permutations
from app import db
from app.models import References, Sources
import matplotlib as mpl
import matplotlib.cm as cm

# Create a network using sources and targets in DB
in_file = db.session.query(References.Source, References.Target).all()
g = net.Graph()

for edge in in_file:
    # Use the first and second value to define the edges
    g.add_edge(edge[0], edge[1])

# Show the degree for each node
node_degree = [n for n in g.degree()]


def degreeColor(value):
    norm = mpl.colors.Normalize(vmin=.04, vmax=1)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(value, bytes=True))


def getNeighborNetwork(verse):
    # Create a new network just for 01001001 and it's network of neighbors
    neighbor_net = net.Graph()

    # Get neighbor of source
    node_neighbors = [n for n in g.neighbors(verse)]

    # Get permutations of edges between neighbors
    perm = permutations(node_neighbors, 2)

    # Loop over each neighbor and add it to a new graph
    for n in g.neighbors(verse):
        neighbor_net.add_edge(verse, n)

    # Loop over each permutation as see if an edge exists in the original network, if so add it to the new one
    for i in list(perm):
        if g.has_edge(i[0], i[1]):
            neighbor_net.add_edge(i[0], i[1])
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
        node_name = db.session.query(Sources.book_name, Sources.chapter, Sources.verse, Sources.norm_degree,
                                     Sources.red_letter) \
            .filter(Sources.Id == n).first()

        if node_name[4] == "TRUE":
            ncolor = "rgba(183, 18, 27, 1.00)"
        else:
            ncolor = "rgba(255,255,255,0.3)"

        color = degreeColor(node_name[3])
        data['nodes'].append({
            "id": n,
            "label": str(node_name[0]) + " " + str(node_name[1]) + ":" + str(node_name[2]),
            "x": pos[n][0],
            "y": pos[n][1],
            "size": node_size[n] * 10,
            "color": ncolor,
            # "color": "rgba"+str(color)
        })

    # Edges
    for i, e in enumerate(neighbor_net.edges):
        data['edges'].append({
            "id": str(i),
            "source": str(e[0]),
            "target": str(e[1]),
            # "color": "rgba(255,255,255,0.007)",
            "size": 10,
            "type": "tapered",  # ['line','curve','arrow','curvedArrow','dashed','dotted','parallel','tapered']
            "edgeColor": 'default',
        })

    return json.dumps(data)
