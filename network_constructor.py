import matplotlib.pyplot as plt
import networkx as ntx

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
            G.add_edge(PN[i], CP_list[i][j])

    # find communities in the graph
    center_node = 0
    max_degree = 0
    # get the center node
    for node in G.nodes:
        if max_degree < G.degree(node):
            max_degree = G.degree(node)
            center_node = node

    remove_disconnected_nodes(G, center_node)
    # #
    # c = girvan_newman(G.copy())
    #
    # # find the nodes forming the communities
    # node_groups = []
    #
    # for i in c:
    #     node_groups.append(list(i))
    # # plot the communities
    # color_map = []
    # for node in G:
    #     if node in node_groups[0]:
    #         color_map.append('blue')
    #     else:
    #         color_map.append('green')
    # #
    pos = ntx.spring_layout(G)
    ntx.draw(G, pos, node_color=label_mark(G.copy(), data), with_labels=True)
    edge_labels = ntx.get_edge_attributes(G, 'weight')

    # ntx.draw(G, node_color=color_map, with_labels=True)
    # plt.show()
    # ntx.draw_networkx(G, with_labels=True, node_color=label_mark(G.copy(), data))
    # draw the array
    edge_labels = ntx.get_edge_attributes(G, 'weight')
    ntx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
    plt.savefig("path.png")


def edge_to_remove(graph):
    G_dict = ntx.edge_betweenness_centrality(graph)
    edge = ()

    # extract the edge with the highest edge betweenness centrality score
    for key, value in sorted(G_dict.items(), key=lambda item: item[1], reverse=True):
        edge = key
        break

    return edge


def girvan_newman(graph):
    # find number of connected components
    sg = ntx.connected_components(graph)
    sg_count = ntx.number_connected_components(graph)

    while sg_count == 1:
        graph.remove_edge(edge_to_remove(graph)[0], edge_to_remove(graph)[1])
        sg = ntx.connected_components(graph)
        sg_count = ntx.number_connected_components(graph)

    return sg


def remove_isolated_nodes(G):
    isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
    G.remove_nodes_from(isolated_nodes)
    return G


def remove_disconnected_nodes(G, node):
    sccs = ntx.weakly_connected_components(G)
    connected_scc = [scc for scc in sccs if node in scc]
    remove_list = []
    for node in G.nodes():
        if node not in connected_scc[0]:
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    return G


def label_mark(G, data) -> list:
    result = []
    for node in G:
        tmp = data[data["Publication Number"] == str(node)]
        label_tmp = tmp.values[0][2]
        if str(label_tmp) == "1":
            result.append("blue")
        else:
            result.append("red")
    print(result)
    return result


main()
