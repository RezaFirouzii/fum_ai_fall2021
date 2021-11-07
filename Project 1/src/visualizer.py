import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self, index, labels, selected_node_id):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        pos = nx.spring_layout(G, seed=3113794652)

        node_color_map = []
        for node in G:
            if 'R' in str(node):
                node_color_map.append('red')
            elif 'G' in str(node):
                node_color_map.append('green')
            elif 'B' in str(node):
                node_color_map.append('black')

        outline_color_map = []
        for node in G:
            if selected_node_id == str(node)[0:len(node)-1]:
                outline_color_map.append('yellow')
            else:
                outline_color_map.append('black')

        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color="whitesmoke")
        nx.draw_networkx(G, pos, edgecolors=outline_color_map, node_color=node_color_map, node_size=500, with_labels=False)
        if index == 0:
            plt.title('initial state')
        else:
            plt.title('state ' + str(index))
        plt.show()


f = open("BfsResult.txt", "r")
text = f.read()
states = text.split("\n")
states.pop(states.index(""))
for stateIndex in states:
    labels = {}
    G = GraphVisualization()
    nodeNeighbors = stateIndex.split(",")
    selectedNodeId = nodeNeighbors[0][0:len(nodeNeighbors[0])-1]
    nodeNeighbors.pop(0)
    for nodeNeighborIndex in nodeNeighbors:
        nodes = nodeNeighborIndex.split(" ")
        if nodes[0]:
            tempStr = nodes[0]
            labels[nodes[0]] = tempStr[0:len(tempStr)-1]
        for nodeIndex in range(1, len(nodes) - 1):
            G.addEdge(nodes[0], nodes[nodeIndex])
    G.visualize(states.index(stateIndex), labels, str(selectedNodeId))
