import spark as sp
import community as comm
import networkx  as nx
import graph_visualization as gv

def get_snap_alg_communities(type, dataset_name) :
    type=type.lower()
    file_name = '/home/sbasodi1/workspace/fall_16_adb_project/adb_comm_detection/alg_outputs/'+type+'_'+dataset_name+'_cmtyvv.txt'

    results_file = open(file_name)
    line_num=-1;
    community={}
    for line in results_file:
        line_num+=1
        nodes=line.split("\t")
        for x in nodes:
            x=x.strip()
            if x.isdigit() :
                key = int(x)
                if not community.has_key(key) :
                    community[key]=[]

                community[key].append(line_num)

    return community

def display_metrics(partition, graph) :
    print 'Modularity: ',comm.modularity(partition, graph)

def update_node_communities(communities, node_graph):
    for (node_id, comm_ids) in communities.iteritems() :
        node_graph.node[node_id]['comm'] = str(comm_ids)
        node_graph.node[node_id]['num_comm'] = len(comm_ids)

def get_community_graph(communities):
    graph = nx.Graph()
    comm_dict= {}
    for (node_id, comm_ids) in communities.iteritems() :
        for comm_id in comm_ids :
           if not comm_dict.has_key(comm_id) :
               comm_dict[comm_id]=[]
           comm_dict[comm_id].append(node_id)
    print "Num of Communities: ", len(comm_dict.keys())
    keys= comm_dict.keys()
    #Create community graph
    for (comm_id, nodes) in comm_dict.iteritems():
        graph.add_node(comm_id)
        graph.node[comm_id]['nodes'] = str(nodes)
        graph.node[comm_id]['num_nodes'] = len(nodes)

    #Add edges
    for (comm_id1, nodes1) in comm_dict.iteritems():
        for (comm_id2, nodes2) in comm_dict.iteritems():
            if comm_id1 != comm_id2 :
                common_nodes = set(nodes1).intersection(set(nodes2))
                if len(common_nodes) >0 :
                    graph.add_edge(comm_id1, comm_id2)
                    graph.edge[comm_id1][comm_id2]['nodes'] = str(list(common_nodes))
                    graph.edge[comm_id1][comm_id2]['num_nodes'] = len(common_nodes)
    for (comm_id, nodes) in comm_dict.iteritems():
        graph.node[comm_id]['conn_comm'] = graph.degree(comm_id)

    return graph


def analyze_dataset(dataset_name, type) :

    if dataset_name == 'facebook':
        dataset_obj = sp.UnDirectedEgoNetworkLoader(dataset_name)
    else:
        dataset_obj = sp.DirectedEgoNetworkLoader(dataset_name)

    # load the network
    dataset_obj.load_network()

    #print sorted(dataset_obj.network.nodes())
    #print (dataset_obj.network.order())
    #print dataset_obj.network.size()

    if type=='all' :
        for t in ['bigclam', 'cesna', 'coda', 'gn','cnm', 'agm'] :
            communities = get_snap_alg_communities(t, dataset_obj.dataset_name)
            display_metrics(communities, dataset_obj.network)
            gv.plot_community(communities, dataset_obj.network)

    elif type=='bp': #Best Partition
        communities = comm.best_partition(dataset_obj.network)
        display_metrics(communities, dataset_obj.network)
        gv.plot_nodes_community_partitions(communities, dataset_obj.network)

    else:
        communities = get_snap_alg_communities(type, dataset_obj.dataset_name)
        #display_metrics(communities, dataset_obj.network)
        comm_graph= get_community_graph(communities)
        update_node_communities(communities, dataset_obj.network)
        gv.show_communities(comm_graph)
        print "Plotting communities.."
        gv.plot_community(comm_graph)
        print "Plotting users with communities.."
        bp = comm.best_partition(dataset_obj.network)
        display_metrics(bp, dataset_obj.network)
        gv.plot_nodes_community_partitions(bp, dataset_obj.network)
        print "Done!!"



if __name__ == '__main__':
    analyze_dataset("facebook", 'bigclam')
    #analyze_dataset("twitter", 'bp')