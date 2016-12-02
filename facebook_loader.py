import spark as sp
import snap
import community as comm
import networkx  as nx

def plot_graph(graph) :
    import  matplotlib.pyplot as plt
    sp = nx.spring_layout(graph)
    plt.axis('off')
    nx.draw(graph, pos=sp, with_labels=False, node_size=35)
    #nx.draw_networkx(graph, pos=sp, with_labels=False, node_size=35)
    plt.show()

def plot_community(partition, graph):
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
'''
def get_snap_graph(dataset_obj) :
    fb_snap = snap.LoadEdgeList(snap.PNGraph, dataset_obj.pathhack + '/facebook_combined.txt', 0, 1)
    nodes = snap.TIntV()
    for node in fb_snap.Nodes():
        nodes.Add(node.GetId())
    print snap.GetModularity(fb_snap, nodes, fb_snap.GetEdges())
'''
def get_snap_alg_partitions(type, dataset_name) :
    type=type.lower()
    file_name = '/home/sbasodi1/workspace/fall_16_adb_project/adb_comm_detection/alg_outputs/'+type+'_'+dataset_name+'_cmtyvv.txt'

    results_file = open(file_name)
    line_num=0;
    partition={}
    partitioned_nodes=[]
    for line in results_file:
        nodes=line.split("\t")
        for x in nodes:
            x=x.strip()
            if x.isdigit() :
                partition[int(x)]=line_num
                partitioned_nodes.append(int(x))

        line_num+=1
    '''
    print "Partitioned nodes:"
    print sorted(partitioned_nodes)
    print "With DUp: ",len(partitioned_nodes)
    print "WithOUT DUp: ",len(set(partitioned_nodes))
    print "UNique nodes: "
    print sorted(set(partitioned_nodes))
    '''
    return partition

def display_metrics(partition, graph) :
    print 'Modularity: ',comm.modularity(partition, graph)


def analyze_dataset(dataset_name, type) :

    if dataset_name == 'facebook':
        dataset_obj = sp.UnDirectedEgoNetworkLoader(dataset_name)
    else:
        dataset_obj = sp.DirectedEgoNetworkLoader(dataset_name)

    # load the network
    dataset_obj.load_network()

    print sorted(dataset_obj.network.nodes())
    print (dataset_obj.network.order())
    #print dataset_obj.network.size()

    # Look at a node's features
    #print len(dataset_obj.network.node[0]['features'])

    # 0: feature not present for this user
    # 1: user does not have this feature
    # 2: user does have this feature

    # look at the features of the whole network

    #print dataset_obj.feature_matrix()
    if type=='all' :
        for t in ['bigclam', 'cesna', 'coda', 'gn','cnm', 'agm'] :
            partition = get_snap_alg_partitions(t, dataset_obj.dataset_name)
            display_metrics(partition, dataset_obj.network)
            plot_community(partition, dataset_obj.network)
    elif type=='bp': #Best Partition
        partition = comm.best_partition(dataset_obj.network)
        display_metrics(partition, dataset_obj.network)
        #plot_community(partition, dataset_obj.network)
    else:
        partition = get_snap_alg_partitions(type, dataset_obj.dataset_name)
        display_metrics(partition, dataset_obj.network)
        plot_community(partition, dataset_obj.network)


    #get_snap_graph()

    #plot_community(partition, dataset_obj.network)

analyze_dataset("twitter", 'bp')