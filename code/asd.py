# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx

#根据pkl文件获取拓扑图,图中将带宽转为了倒数
def read_pickle(pickle_path):
    pkl_graph = nx.read_gpickle(pickle_path)
    return pkl_graph

if __name__ == '__main__':
    data = read_pickle('E:\学术12.16\code\D3QN\Experimental Dataset/node14_data\90-2022-03-11-19-50-52.pkl')
    for i in data.edges.data():
        print(f"{i},")


#32-2022-03-11-19-45-04.pkl    10
#46-2022-03-11-19-46-28.pkl    20
#71-2022-03-11-19-48-58.pkl    30
#104-2022-03-11-19-52-16.pkl   40
#121-2022-03-11-19-53-58.pkl

# import matplotlib.pyplot as plt
# import networkx as nx
#
#
# def create_simple_network_graph():
#     # Network data: (source, dest, {metrics})
#     network_data = [
#         (4, 5, {'bw': 29.999715020779735, 'delay': 3.353238105773926, 'loss': 0.0}),
#         (4, 11, {'bw': 26.480421219319084, 'delay': 7.2144269943237305, 'loss': 0.0}),
#         (4, 7, {'bw': 0.9661224975222584, 'delay': 1970.0974225997925, 'loss': 0.003088399006393639}),
#         (4, 2, {'bw': 6.7799342444048145, 'delay': 15.701651573181152, 'loss': 7.63216372082495}),
#         (4, 6, {'bw': 0.020510604241772867, 'delay': 752.077579498291, 'loss': 6.52305199151684}),
#         (4, 1, {'bw': 0, 'delay': 21.942734718322754, 'loss': 0.003864624670461855}),
#         (4, 9, {'bw': 23.664538613861392, 'delay': 19.987106323242188, 'loss': 0.0}),
#         (5, 6, {'bw': 23.9997118847539, 'delay': 9.568572044372559, 'loss': 0.00026687892437118324}),
#         (5, 7, {'bw': 18.6563171456888, 'delay': 9.150266647338867, 'loss': 0.031623069984612937}),
#         (5, 2, {'bw': 7.031867146858865, 'delay': 20.346522331237793, 'loss': 4.300155439791168}),
#         (5, 8, {'bw': 0.010158526821438585, 'delay': 1202.655553817749, 'loss': 5.872086445841551}),
#         (5, 1, {'bw': 9.099462497526215, 'delay': 16.753673553466797, 'loss': 0.005044659712225186}),
#         (9, 7, {'bw': 20.997490693069306, 'delay': 2.76792049407959, 'loss': 0.0}),
#         (9, 10, {'bw': 3.0486256186894476, 'delay': 8.850812911987305, 'loss': 0.0}),
#         (9, 13, {'bw': 0, 'delay': 434.3000650405884, 'loss': 0.0006511502685302192}),
#         (9, 1, {'bw': 0.692931485148339, 'delay': 12.615799903869629, 'loss': 0.005300050313721479}),
#         (7, 8, {'bw': 3.4809719775820014, 'delay': 16.892552375793457, 'loss': 7.190302645906815}),
#         (11, 1, {'bw': 0.0351733966746135, 'delay': 861.6377115249634, 'loss': 0.0}),
#         (6, 2, {'bw': 0, 'delay': 555.2370548248291, 'loss': 0.007727797713017911}),
#         (13, 12, {'bw': 17.696977425742517, 'delay': 10.873675346374512, 'loss': 0.0027158707759764107}),
#         (1, 3, {'bw': 0, 'delay': 8.00323486328125, 'loss': 0.0024393319920445362}),
#         (14, 12, {'bw': 22.237324361765285, 'delay': 15.455961227416992, 'loss': 3.123423662499008}),
#         (14, 8, {'bw': 0.8962018018018192, 'delay': 309.5747232437134, 'loss': 0.0})
#     ]
#
#     # Create graph
#     G = nx.Graph()
#
#     # Add edges
#     for src, dst, metrics in network_data:
#         G.add_edge(src, dst)
#
#     # Set up the plot
#     plt.figure(figsize=(12, 8))
#
#     # Create layout
#     pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
#
#     # Manual adjustment for better visualization
#     pos_adjusted = {
#         1: (-0.8, 0.2), 2: (-0.3, 0.8), 3: (-1.0, -0.2), 4: (0.0, 0.0),
#         5: (0.8, 0.3), 6: (1.0, 0.8), 7: (0.2, -0.8), 8: (0.8, -0.6),
#         9: (-0.2, -0.5), 10: (-0.8, -0.8), 11: (0.3, 0.8), 12: (1.2, 0.0),
#         13: (0.6, -0.3), 14: (1.4, -0.2)
#     }
#
#     # Use adjusted positions
#     for node in G.nodes():
#         if node in pos_adjusted:
#             pos[node] = pos_adjusted[node]
#
#     # Draw edges - all same color and thickness
#     nx.draw_networkx_edges(G, pos, edge_color='#666666', width=2.0, alpha=0.7)
#
#     # Draw nodes
#     nx.draw_networkx_nodes(G, pos, node_color='lightgreen',
#                            node_size=1000, alpha=0.9, edgecolors='black', linewidths=2)
#
#     # Draw node labels
#     nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')
#
#     plt.axis('off')
#     plt.tight_layout()
#     plt.show()
#
#
# if __name__ == "__main__":
#     create_simple_network_graph()
