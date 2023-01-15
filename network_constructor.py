import matplotlib.pyplot as plt
import networkx as ntx

import label

G = ntx.Graph()
plt.rcParams.update({
    'figure.figsize': (12, 12)
})
data = label.label()
CP = data["CP"].values
PN = data["Publication Number"]
Label = data["label"]
CP_list = []
for i in CP:
    CP_list.append(i.split("'")[1::2])

for i in range(len(PN)):
    for j in range(len(CP_list[i])):
        if PN[i] == CP_list[i][j]:
            print(PN[i])
            continue
        G.add_edge(PN[i], CP_list[i][j])
colors = []
print(G.nodes())
ntx.draw(G, with_labels=True)
plt.savefig("path.png")
