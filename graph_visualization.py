import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from networkx_viewer import Viewer
import matplotlib.pyplot as plt
import Tkinter as Tk
import networkx as nx
from tkMessageBox import showinfo

def show_communities(communities) :
    app = Viewer(communities, title="Community Viewer", home_node=50, levels=100)
    # app = GraphViewerApp(G, home_node='a', levels=2)
    app.mainloop()
def plot_community(partition):
    import  matplotlib.pyplot as plt

    num_of_partitions= len(partition.nodes())
    partition_color = [float(x) / (num_of_partitions - 1) for x in range(num_of_partitions)]
    node_color_values = [float(node)/(num_of_partitions-1) for node in partition.nodes() ]
    node_labels = dict([(node, node) for node in partition.nodes()])

    edge_labels = dict([((u, v,), d['num_nodes']) for u, v, d in partition.edges(data=True)])
    # Edges with more than 70% similarity are shown red
    red_edges = []
    widths = []
    for n1, n2, w in (partition.edges_iter(data='num_nodes', default=1)):
        #widths.append(w * w * 10)
        if (w > 10):
            red_edges.append((n1, n2))

    edge_colors = ['black' if not edge in red_edges else 'red' for edge in partition.edges()]

    plt.axis('off')
    sp = nx.spring_layout(partition)
    nx.draw_networkx_labels(partition,pos=sp, labels=node_labels)
    #nx.draw_networkx_edge_labels(partition,pos=sp, edge_labels=edge_labels)

    ec = nx.draw_networkx_edges(partition, pos=sp, alpha=0.1)
    nc = nx.draw_networkx_nodes(partition, pos=sp, node_color=node_color_values,
                                 cmap=plt.cm.jet)
    nx.draw(partition, pos=sp, node_color=node_color_values, node_size=30,
            edge_color=edge_colors, with_labels=False)

    #plt.colorbar(nc, ticks=partition_color )
    plt.show()

def plot_nodes_community(partition, graph):
    import  matplotlib.pyplot as plt

    num_of_partitions= len(set(partition.values()))
    partition_color = [float(x) / (num_of_partitions - 1) for x in range(num_of_partitions)]
    node_color_values = [float(partition[node])/(num_of_partitions-1) for node in graph.nodes() ]

    plt.axis('off')
    sp = nx.spring_layout(graph)
    ec = nx.draw_networkx_edges(graph, pos=sp, alpha=0.1)
    nc = nx.draw_networkx_nodes(graph, pos=sp, node_color=node_color_values,
                                with_labels=False, cmap=plt.cm.jet)
    plt.colorbar(nc, ticks=partition_color )
    plt.show()
