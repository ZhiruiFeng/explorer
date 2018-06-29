## Some functions for analyzing the property of graph
import networkx as nx
import random
from random import choice
import matplotlib.pyplot as plt

def connectivity_info(G):
    if nx.is_strongly_connected(G):
        print("A strongly connected graph.")
    elif nx.is_weakly_connected(G):
        print("A weakly connected graph.")
    else:
        num = nx.number_strongly_connected_components(G)
        print("Not a strongly connected graph, have {} component".format(num))

def largest_strongly_conencted_component(G):
    if nx.is_strongly_connected(G):
        print("A strongly connected graph.")
        return(G)
    else:
        num = nx.number_strongly_connected_components(G)
        print("Not a strongly connected graph, have {} components".format(num))
        largest = max(nx.strongly_connected_components(G), key=len)
        Component = G.subgraph(largest)
        num_nodes = len(Component.nodes())
        num_edges = len(Component.edges())
        print("The largest components:")
        print("Nodes: {}".format(num_nodes))
        print("Edges: {}".format(num_edges))
        return(Component)

def largest_connected_component_undirected(G):
    if nx.is_connected(G):
        print("A connected graph.")
        return(G)
    else:
        num = nx.number_connected_components(G)
        print("Not a connected graph, have {} components".format(num))
        largest = max(nx.connected_components(G), key=len)
        Component = G.subgraph(largest)
        num_nodes = len(Component.nodes())
        num_edges = len(Component.edges())
        print("The largest components:")
        print("Nodes: {}".format(num_nodes))
        print("Edges: {}".format(num_edges))
        return(Component)

def readDiGraph(infile):
    G = nx.DiGraph()
    with open(infile) as f:
        l = f.readline()
        while l:
            if l[0] == '#':
                l = f.readline()
                continue
            items = l.strip().split()
            if len(items) == 3:
                node1, node2, weight = items
            elif len(items) == 2:
                node1, node2 = items
                weight = 1.0
            else:
                l = f.readline()
                continue
            G.add_edge(node1, node2, weight=float(weight))
            l = f.readline()
    return G

def readgraph(infile):
    G = nx.Graph()
    with open(infile) as f:
        l = f.readline()
        while l:
            if l[0] == '#':
                l = f.readline()
                continue
            items = l.strip().split()
            if len(items) == 3:
                node1, node2, weight = items
            elif len(items) == 2:
                node1, node2 = items
                weight = 1.0
            else:
                l = f.readline()
                continue
            G.add_edge(node1, node2, weight=float(weight))
            l = f.readline()
    return G

def writeDiGraph(G, outfile):
    outfile = open(outfile, 'w')
    print("Start writing into file {}".format(outfile))
    for edge in G.edges():
        node1, node2 = edge
        if 'weight' in G[node1][node2].keys():
            weight = G[node1][node2]['weight']
        else:
            weight = 1.0
        outfile.write(str(node1)+" "+str(node2)+" "+str(weight)+"\n")
    outfile.close()

def drawGraph(G):
    pos = nx.spring_layout(G)
    #nx.draw_networkx_nodes(G, pos, node_size=300)
    #nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_nodes(G, pos, node_size=4)
    nx.draw_networkx_edges(G, pos, width=1)
    #nx.draw_networkx_edge_labels(G, pos, width=1, edge_labels=nx.get_edge_attributes(G,'weight'))
    #nx.draw_networkx_labels(G, pos, labels=nodes_label,font_size=6, font_family='sans-serif')
    plt.axis('off')
    plt.show()

def generate_random_digraph(n, p, low, high):
    for i in range(100):
        G = nx.gnp_random_graph(n, p, directed = True)
        if nx.is_strongly_connected(G):
            break
    if nx.is_strongly_connected(G) == False:
        print("Unable to generate strongly connected graph, try increase 'p'.")
    density = float(len(G.edges()))/(n*(n-1))
    print("Density: {}".format(density))
    for (n1, n2) in G.edges():
        G[n1][n2]['weight']=random.randint(low, high)
    return G, density

def distance_info(G):
    dis = []
    for node in list(G.nodes()):
        length = nx.single_source_dijkstra_path_length(G, node)
        dis.extend(list(length.values()))
    x = list(set(dis))
    y = []
    for i in x:
        y.append(dis.count(i))
    y[0]=0
    s = sum(y)
    for i in range(len(y)):
        y[i] = float(y[i])/s
    plt.plot(x,y,'r-o', linewidth=1)
    plt.xlabel('distance')
    plt.ylabel('count (persents)')
    plt.title('Statistic of pair distances')
    plt.show()

if __name__ == "__main__":
    in_directory = "../test/raw/"
    out_directory = "../test/"
    name = "p2p-Gnutella08.txt"
    infile = in_directory + name
    G = readDiGraph(infile)
    print("Finish reading")
    connectivity_info(G)
    largest = largest_strongly_conencted_component(G)
    num_nodes = len(largest.nodes())
    num_edges = len(largest.edges())
    outfile = out_directory+name.strip().split('.')[0]+'_'+str(num_nodes)+'_'+str(num_edges)
    writeDiGraph(largest, outfile)
