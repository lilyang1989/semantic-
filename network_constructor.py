import matplotlib.pyplot as plt
import networkx as ntx
import networkx as nx

import label


def main():
    G = ntx.DiGraph()
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
    #
    # 计算边的权重，根据度的大小
    # 将每个节点的度作为其权重
    weights = dict(G.degree())
    # 将权重添加到边上
    for u, v in G.edges():
        G.edges[u, v]['weight'] = weights[u] + weights[v]
    #
    #
    # 这一步是提取网络中包含最大度的弱连通网络
    # get the biggest degree node from the graph
    # 找到出度最大的节点
    max_out_degree_nodes = get_high_degree_nodes(G, 6)
    path = extract_main_path(G.copy(), max_out_degree_nodes[2], data)
    # depict  the path use the matplotlib
    visualize_main_path(G, path, data, max_out_degree_nodes[2])


def label_mark(G, data, max_node, paths) -> list:
    result = []
    for node in G:
        tmp = data[data["Publication Number"] == str(node)]
        label_tmp = tmp.values[0][2]
        if node == max_node:
            result.append('black')
            print(str(label_tmp))
            continue
        if str(label_tmp) == "1":
            result.append("blue")
        else:
            result.append("red")
    print(result)
    return result


def calculate_spc_weight(graph, path):
    weight = 1
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i + 1])
        weight *= edge_data['weight']
    return weight


def find_nodes_with_min_degree(graph):
    min_degree = float('inf')
    min_degree_nodes = []
    for node in graph:
        out_degree = len(graph[node])
        in_degree = 0
        for other_node in graph:
            if node in graph[other_node]:
                in_degree += 1
        degree = out_degree + in_degree
        if degree < min_degree:
            min_degree = degree
            min_degree_nodes = [node]
        elif degree == min_degree:
            min_degree_nodes.append(node)
    return min_degree_nodes


# label为1则应该是起始点，label为2则应该是结束点
def extract_starts_ends(all: list, data) -> tuple:
    starts = []
    ends = []
    for node in all:
        tmp = data[data["Publication Number"] == str(node)]
        label_tmp = tmp.values[0][2]
        if str(label_tmp) == "1":
            starts.append(node)
        else:
            ends.append(node)
    return starts, ends


def get_high_degree_nodes(G, k):
    """
    返回 networkx 中度数比较大的点列表。

    参数：
        - G：networkx 图形对象。
        - k：int，要返回的前k个最高度数的节点。

    返回值：
        - 一个包含前k个最高度数节点的列表。
    """
    degrees = dict(G.degree())
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    return sorted_nodes[:k]


def extract_main_path(G, max_out_degree_node, data):
    # 提取包含指定节点的弱连通图，b_subgraph
    b_subgraph = None
    node = max_out_degree_node
    sccs = nx.weakly_connected_components(G)
    for scc in sccs:
        if node in scc:
            b_subgraph = G.subgraph(scc)
            break

    #
    #
    #
    # # 使用Dijkstra算法寻找最短路径，并提取主路径
    #
    # 第一步是确定start的node，一般来说是时间较早的
    #
    starts_ends = find_nodes_with_min_degree(b_subgraph.copy())
    starts, ends = extract_starts_ends(starts_ends, data)
    mid = max_out_degree_node
    print(starts, ends)
    paths_back = []
    for end in ends:
        try:
            path = nx.dijkstra_path(G.copy(), mid, end)
            paths_back.append(path)
        except Exception as e:
            print(e)
    paths_forward = []
    for start in starts:
        try:
            path = nx.dijkstra_path(G.copy(), start, mid)
            paths_back.append(path)
        except Exception as e:
            print(e)
    print(f"向前路线有{len(paths_forward)},向后有{len(paths_back)}")
    print(paths_back)
    #
    # 在已经找到的前后路径中找出度数最大的
    #
    max_B_path = []
    max_B_degree = 0
    for path in paths_back:
        if calculate_spc_weight(b_subgraph, path) > max_B_degree:
            max_B_path = path
            max_B_degree = calculate_spc_weight(b_subgraph, path)
    #
    max_F_path = []
    max_F_degree = 0
    for path in paths_forward:
        if calculate_spc_weight(b_subgraph, path) > max_F_degree:
            max_F_path = path
            max_F_degree = calculate_spc_weight(b_subgraph, path)
    Final_path = max_F_path + max_B_path
    print(Final_path)
    return Final_path
    # pos = ntx.spiral_layout(b_subgraph)
    # ntx.draw(b_subgraph, pos=pos, node_color=label_mark(b_subgraph, data, max_out_degree_node), with_labels=True)
    # edge_labels = ntx.get_edge_attributes(G, 'weight')
    # # ntx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #
    # plt.show()
    # plt.savefig("path.png")


def visualize_main_path(G, path, data, max_out_degree_node):
    pos = ntx.spiral_layout(G)
    labels = label_mark(G, data, max_out_degree_node, path
                        )
    ntx.draw(G, pos=pos, node_color=labels, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)], width=10, alpha=0.5,
                           edge_color='yellow')
    plt.show()
    plt.savefig("path.png")
    # pos = nx.spring_layout(G)
    # node_color = label_mark(G, data, path[len(path) // 2])
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_color)
    # nx.draw_networkx_labels(G, pos, font_size=20)
    # nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)], width=5, alpha=0.5,
    #                        edge_color='red')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.2)
    # plt.show()


if __name__ == '__main__':
    main()
