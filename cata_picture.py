import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# 被引用的
CITED = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
color_dict = {
    'AR': 'red',
    'MR': 'blue',
    'SZ': 'yellow',
    'VR': 'black'
}
Type_dict = {
    'AR': 0,
    'MR': 1,
    'SZ': 2,
    'VR': 3
}

# 读取数据
df_1 = pd.read_excel('label_result/AR.xlsx')
df_2 = pd.read_excel('label_result/MR.xlsx')
df_3 = pd.read_excel('label_result/SZ.xlsx')
df_4 = pd.read_excel('label_result/VR.xlsx')
df = pd.concat([df_1, df_2, df_3, df_4])
# 创建空的有向图
G = nx.DiGraph()
CP = df["CP"].values
PN = df["Publication Number"].tolist()
CP_list = []
node_colors = []
nodes = []
# convert str to list
for i in CP:
    if type(i) == float:
        CP_list.append([])
        continue
    CP_list.append(i.split("'")[1::2])
# load the data to networkx
for i in range(len(PN)):
    G.add_node(PN[i])
    label_PN = df.loc[df['Publication Number'] == PN[i], 'label'].tolist()[0]
    print(label_PN)
    if PN[i] not in nodes:
        node_colors.append(color_dict.get(label_PN, 'grey'))
    nodes.append(PN[i])
    #
    for j in range(len(CP_list[i])):
        if PN[i] == CP_list[i][j]:
            continue
        label_CP = df.loc[df['Publication Number'] == CP_list[i][j], 'label'].tolist()
        if CP_list[i][j] not in nodes:
            if len(label_CP) == 0:
                node_colors.append('grey')
            else:
                print(label_CP)
                node_colors.append(color_dict.get(label_CP[0], 'grey'))
        nodes.append(CP_list[i][j])
        # 添加引用关系
        if len(label_CP) == 0:
            label_CP = ["SSS"]
        CITED[Type_dict.get(label_CP[0], 4)][Type_dict.get(label_PN, 4)] += 1
        G.add_edge(CP_list[i][j], PN[i])

print(CITED)
# 绘制网络图
pos = nx.spring_layout(G)
plt.figure(figsize=(50, 50))
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, width=0.5)
nx.draw_networkx_nodes(G, pos, node_color=node_colors)
plt.axis('off')
plt.show()
plt.savefig("FOUR.png")
