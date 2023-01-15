import matplotlib.pyplot as plt
import networkx as ntx

import label

G = ntx.Graph()
plt.rcParams.update({
    'figure.figsize': (30, 30)

})
data = label.label()
CP = data["CP"].values
PN = data["Publication Number"]
Label = data["label"]
CP_list = []
for i in CP:
    if type(i) == float:
        CP_list.append([])
        continue
    CP_list.append(i.split("'")[1::2])
colors = []
for i in range(len(PN)):
    if Label[i] == "2":
        G.add_node(PN[i])
        colors.append("red")
    else:
        G.add_node(PN[i])
        colors.append("blue")
    for j in range(len(CP_list[i])):
        if PN[i] == CP_list[i][j]:
            continue
        G.add_edge(PN[i], CP_list[i][j])
ntx.draw_networkx(G, with_labels=True, node_color=colors)
plt.savefig("path.png")
