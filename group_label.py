from collections import Counter

import community
import matplotlib.pyplot as plt
import networkx as ntx
import networkx as nx

import label


def main():
    G = ntx.Graph()
    plt.rcParams.update({
        'figure.figsize': (30, 30)
    })
    data = label.label()
    CP = data["CP"].values
    PN = data["Publication Number"]
    CP_list = []
    # convert str to list
    for i in CP:
        if type(i) == float:
            CP_list.append([])
            continue
        CP_list.append(i.split("'")[1::2])
    # load the data to networkx
    for i in range(len(PN)):
        G.add_node(PN[i])
        for j in range(len(CP_list[i])):
            if PN[i] == CP_list[i][j]:
                continue
            G.add_edge(CP_list[i][j], PN[i])
    #
    picture(G)


def picture(G):
    degrees = dict(G.degree())
    # 找到度最大的节点
    max_degree_node = max(degrees, key=degrees.get)
    # 获取与节点node相连通的所有节点集合
    connected_nodes = set()
    for component in nx.connected_components(G):
        if max_degree_node in component:
            connected_nodes.update(component)
    G = G.subgraph(connected_nodes)
    partition = community.best_partition(G)
    # 计算模块度
    modularity = community.modularity(partition, G)
    print("Best modularity:", modularity)
    # 提取top3
    top4 = Counter(partition.values()).most_common(4)
    # print(len(G.nodes))
    # print(top3)
    top4_communities = [k for k, v in partition.items() if v in [c[0] for c in top4]]
    G = G.subgraph(top4_communities)

    # # 存儲top3
    # res = [[], [], [], []]
    # for node in G.nodes():
    #     num = partition[node]
    #     if num == top4[0][0]:
    #         res[0].append(node)
    #     if num == top4[1][0]:
    #         res[1].append(node)
    #     if num == top4[2][0]:
    #         res[2].append(node)
    #     if num == top4[3][0]:
    #         res[3].append(node)
    # print(res)
    # # # 将列表保存到文件中
    # with open('top4.pkl', 'wb') as f:
    #     pickle.dump(res, f)
    # # print(top3_communities)
    # 创建字典存储颜色
    color_map = {}
    for node in G.nodes():
        if node in top4_communities:
            if partition[node] == top4[0][0]:
                color_map[node] = 'red'
            elif partition[node] == top4[1][0]:
                color_map[node] = 'yellow'
            elif partition[node] == top4[2][0]:
                color_map[node] = 'blue'
            else:
                color_map[node] = 'green'
        else:
            color_map[node] = 'white'
            continue  # skip white nodes

    # 过滤掉白色节点
    # create a new subgraph with non-white nodes and their edges

    # 调整节点大小并绘制带有社区颜色的图形
    pos = nx.spring_layout(G)
    node_size = [100 if partition[node] in top4_communities else 1 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=list(color_map.values()), node_size=node_size)
    nx.draw_networkx_edges(G, pos, width=0.1)
    print("down!!!!!!!!!!!!!!")
    plt.show()


main()
