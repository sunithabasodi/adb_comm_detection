import networkx as nx
from networkx_viewer import Viewer

### Example 1 ####
G = nx.Graph()
lines = ["1 2","3 4", "2 3", "4 2"]
G1 = nx.parse_edgelist(lines, nodetype = int)
G.add_edges_from(G1.edges(), weight='23')
G.node[1]['name']='one'
G.node[2]['name']='two'
G.node[3]['name']='three'
G.node[1]['group']='a'
G.node[2]['group']='a'
G.node[3]['group']='k'

app = Viewer(G, title="Community Viewer", home_node=1,levels=100)
#app = GraphViewerApp(G, home_node='a', levels=2)
app.mainloop()
