# -*- coding:utf-8 -*-

#import networkx as nx
# import networkx.algorithms.approximation as na
# import copy
# import pandas as pd
import numpy as np
# import time
# import random
#
# import setting
import DQN_tools
import torch
import matplotlib.pyplot as plt
import rl_utils
#
from getreward import GetReward
from getreward import GetMinbw
from getreward import GetMaxdelay
from getreward import GetMaxloss
# from asd import read_pickle


import networkx as nx
import random
import csv
import os




def save_to_csv(file_path, data_list):
    # 读取现有数据（如果有的话）
    existing_data = []
    try:
        with open(file_path, "r", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                existing_data.append(row)
    except FileNotFoundError:
        # 如果文件不存在，创建一个空的现有数据列表
        existing_data = []

    # 将新的 data_list 追加到现有数据的每一行
    for i, data in enumerate(data_list):
        if i < len(existing_data):
            existing_data[i].append(data)
        else:
            existing_data.append([data])

    # 将更新后的数据写回文件
    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)
# 根据pkl文件获取拓扑图



def read_pickle(pickle_path):
    return nx.read_gpickle(pickle_path)


# 获取拓扑中的随机源节点和指定数量的目的节点
def get_sw_list(graph,num_destinations, src_sw, dst_sw1):
    sw_list = [src_sw, dst_sw1]
    for i in range(1, num_destinations):  # n副本模式，如n=3，3副本模式下，需要添加（1，2）共两个新的目的节点。
        sw_next = (dst_sw1 + 3*i) % 10
        if sw_next == 0:
            sw_next = 10
        sw_list.append(sw_next)
    return sw_list


# 计算指定路径的信息
def get_path_info(graph, path):
    total_delay = 0
    total_loss = 0
    min_bw = float('inf')

    path_edges = list(zip(path[:-1], path[1:]))

    for edge in path_edges:
        edge_data = graph.get_edge_data(*edge)
        if edge_data:
            total_delay += edge_data['delay']
            total_loss += edge_data['loss']
            min_bw = min(min_bw, edge_data['bw'])

    return total_delay, total_loss, min_bw



def count_repeated_edges(multicast_tree):
    edge_counts = {}

    # 将每条路径转换为边的列表并计数
    for path in multicast_tree:
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            if edge in edge_counts:
                edge_counts[edge] += 1
            else:
                edge_counts[edge] = 1

    # 计算重复边的总数
    repeated_edge_count = sum(count - 1 for count in edge_counts.values() if count > 1)

    return repeated_edge_count

def _one_hot(sw_list, node, nodes, size):
    x = torch.zeros(size)
    # 所有节点标记为16
    i = 1
    for i in nodes:
        x[i - 1] = 16  # x变为tensor([16., 16., 16., 16., 16., 16., 16., 16., 16., 16., 16., 16., 16., 16.])
    x[10] = 16
    x[sw_list[0] - 1] = 17
    x[sw_list[1] - 1] = 18
    x[sw_list[2] - 1] = 18
    x[sw_list[3] - 1] = 18
    x[node] = 19
    #print("x",x)
    return x



def select_k_paths(graph, sw_list, k):
    # 将源节点赋值给src
    src = sw_list[0]
    # 将目标节点赋值给d1, d2, d3
    d1, d2, d3 = sw_list[1], sw_list[2], sw_list[3]
    # 初始化保存路径的变量
    paths_to_all = []
    paths_to_d1 = []
    paths_to_d2 = []
    paths_to_d3 = []

    print("选k条路径")

    # 计算图中所有边的最大带宽、最小时延和最大丢包率，用于归一化
    min_bw = GetMinbw(graph)
    max_delay = GetMaxdelay(graph)
    max_loss = GetMaxloss(graph)

    # 函数用于计算路径权重
    def path_weight(path):
        weight = 0
        for i in range(len(path) - 1):
            edge_data = graph[path[i]][path[i+1]]
            # 带宽归一化，带宽越大，值越小
            if edge_data['bw'] == 0:
                norm_bw = 1
            else:
                norm_bw = min_bw / edge_data['bw']
            # 时延归一化，时延越小，值越小
            norm_delay = edge_data['delay'] / max_delay
            # 丢包率归一化，丢包率越小，值越小
            norm_loss = edge_data['loss'] / max_loss
            # 综合权重
            weight += norm_bw + norm_delay + norm_loss
        return weight

    # 函数用于选取k条路径
    def get_k_paths(all_paths, k):
        # 按路径权重排序
        all_paths.sort(key=path_weight)
        if len(all_paths) >= k:
            return all_paths[:k]
        else:
            extended_paths = all_paths * (k // len(all_paths)) + all_paths[:k % len(all_paths)]
            return extended_paths[:k]

    # 寻找并保存从源节点到每个目标节点的所有路径
    for target_node in [d1, d2, d3]:
        all_paths = list(nx.all_simple_paths(graph, src, target_node))
        if target_node == d1:
            paths_to_d1.extend(all_paths)
        elif target_node == d2:
            paths_to_d2.extend(all_paths)
        elif target_node == d3:
            paths_to_d3.extend(all_paths)

    # 从每个目标节点的路径中选取k条路径加入到paths_to_all中
    paths_to_all.extend(get_k_paths(paths_to_d1, k))
    paths_to_all.extend(get_k_paths(paths_to_d2, k))
    paths_to_all.extend(get_k_paths(paths_to_d3, k))
    # 给每一条路径编号
    path_indices = {i: paths_to_all[i] for i in range(len(paths_to_all))}

    return paths_to_all, paths_to_d1, paths_to_d2, paths_to_d3, path_indices
# def select_k_paths(graph, sw_list, k):
#     # 将源节点赋值给src
#     src = sw_list[0]
#     # 将目标节点赋值给d1, d2, d3
#     d1, d2, d3 = sw_list[1], sw_list[2], sw_list[3]
#     # 初始化保存路径的变量
#     paths_to_all = []
#     paths_to_d1 = []
#     paths_to_d2 = []
#     paths_to_d3 = []
#     print ("graph",graph)
#     # 函数用于选取k条路径
#     def get_k_paths(all_paths, k):
#         all_paths.sort(key=len)  # 按路径长度排序
#         if len(all_paths) >= k:
#             return all_paths[:k]
#         else:
#             extended_paths = all_paths * (k // len(all_paths)) + all_paths[:k % len(all_paths)]
#             return extended_paths[:k]
#         #if len(all_paths) >= k:
#             #return random.sample(all_paths, k)
#         #else:
#             #extended_paths = all_paths * (k // len(all_paths)) + all_paths[:k % len(all_paths)]
#             #return random.sample(extended_paths, k)
#
#     # 寻找并保存从源节点到每个目标节点的所有路径
#     for target_node in [d1, d2, d3]:
#         #all_paths = list(nx.all_simple_paths(graph, src, target_node))
#         all_paths = list(nx.all_simple_paths(graph, src, target_node))
#         if target_node == d1:
#             paths_to_d1.extend(all_paths)
#         elif target_node == d2:
#             paths_to_d2.extend(all_paths)
#         elif target_node == d3:
#             paths_to_d3.extend(all_paths)
#
#     # 从每个目标节点的路径中选取k条路径加入到paths_to_all中
#     paths_to_all.extend(get_k_paths(paths_to_d1, k))
#     paths_to_all.extend(get_k_paths(paths_to_d2, k))
#     paths_to_all.extend(get_k_paths(paths_to_d3, k))
#     # 给每一条路径编号
#     path_indices = {i: paths_to_all[i] for i in range(len(paths_to_all))}
#
#     return paths_to_all, paths_to_d1, paths_to_d2, paths_to_d3, path_indices
# # 计算最短路径并获取路径信息
# def calculate_paths_info(graph, sw_list):
#     src = sw_list[0]
#     dsts = sw_list[1:]
#     paths_info = []
#     paths = []
#     for dst in dsts:
#         try:
#             path = nx.shortest_path(graph, src, dst, weight='delay')
#             paths.append(path)
#             delay, loss, min_bw = get_path_info(graph, path)
#             paths_info.append((delay, loss, min_bw))
#         except nx.NetworkXNoPath:
#             paths.append(None)
#             paths_info.append((float('inf'), float('inf'), float('inf')))
#     print("paths",paths)
#     print("paths_info",paths_info)
#     return paths, paths_info

# 计算最短路径并获取路径信息
def calculate_paths_info(graph, multicast_path):
    paths_info = []
    for path in multicast_path:
        try:
            delay, loss, min_bw = get_path_info(graph, path)
            paths_info.append((delay, loss, min_bw))
        except nx.NetworkXNoPath:
            paths_info.append((float('inf'), float('inf'), float('inf')))
    print("paths_info",paths_info)
    return paths_info

def D3QN(graph, sw_list):
    print ("进来了")
    print ("sw_list", sw_list)


    #self.graph = self.topology_awareness.graph
    #print ("graph:", graph)
    # 检查数据类型
    #print("graph type:", type(graph))

    # 如果数据是字典，打印键
    if isinstance(graph, dict):
        print("data keys:", graph.keys())

    # 如果数据是列表，打印长度
    if isinstance(graph, list):
        print("data length:", len(graph))

    # 打印具体的数据
    print("data:", graph)


    # 检查self.graph
    print("graph:",graph)
    # 打印图对象的基本信息
    print("Number of nodes:", graph.number_of_nodes())
    print("Number of edges:", graph.number_of_edges())
    print("Nodes:", graph.nodes(data=True))
    print("Edges:", graph.edges(data=True))

    # -*- coding: utf-8 -*-
    # 将源节点赋值给src
    src = sw_list[0]
    # 将目标节点赋值给d1, d2, d3
    d1, d2, d3 = sw_list[1:]
    goal_node =d3
    lr = 0.001
    num_episodes = 500
    hidden_dim = 128
    # 未来状态对Q值的影响系数
    gamma = 0.9
    epsilon = 0.95
    target_update = 200
    buffer_size = 150
    minimal_size = 100
    batch_size = 64
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device(
        "cpu")
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    replay_buffer = DQN_tools.ReplayBuffer(buffer_size)
    k=50
    paths_to_all, paths_to_d1, paths_to_d2, paths_to_d3, path_indices = select_k_paths(graph=graph,
                                                                              sw_list=sw_list,k=k)



    state_dim = len(graph.nodes) + 1
    action_dim = len(paths_to_all)
    agent = DQN_tools.DQN(state_dim, hidden_dim, action_dim, lr, gamma, epsilon,
                          target_update, device,'D3QN')
    study_total = 0
    return_list = []
    repeated_list = []
    delay_list = []
    bw_list = []

    for i in range(15000):
        study_flag = 0
        episode_return = 0
        step = 1
        done = False
        # set current state
        pathselect_all = []
        multicast_tree = []
        current_node = d1
        current_state = _one_hot(sw_list, current_node - 1,graph.nodes,len(graph.nodes) + 1).to(device)
        if study_total % 100 == 0:
            #epsilon = epsilon * 0.957
            epsilon = epsilon * 0.951
        episode_return = 0
        finish = False
        while not finish:
            if current_node == 11:
                done = True
                break
            #print "一次学习"
            study_total = study_total + 1
            pathselect_all = []
            # 遍历所有路径，选择符合条件的路径
            for index, path in path_indices.items():
                if path[-1] == current_node:
                    pathselect_all.append((index, path))
            if np.random.uniform() < epsilon:
                #print "探索："
                selected_index, pathselect = random.choice(pathselect_all)
                action = selected_index
            else:
                #print "经验："

                current_state = _one_hot(sw_list, current_node - 1,graph.nodes,len(graph.nodes) + 1).to(device)
                # 获取所有动作的Q值
                q_values = agent.q_net(current_state)


                # 去除第一维的单个维度，确保 q_values 是一维的
                q_values = q_values.squeeze(0)

                # 根据current_state选择不同范围的动作
                if current_node == sw_list[1]:
                    action = q_values[0:k].argmax().item()
                elif current_node == sw_list[2]:
                    action = q_values[k:2*k].argmax().item() + k
                elif current_node == sw_list[3]:
                    action = q_values[2*k:3*k].argmax().item() + 2*k
                #print "action:", action
                #action = agent.q_net(current_state).argmax().item()

            # 将 action 添加到 multicast_tree
            multicast_tree.append(path_indices[action])

            # 初始化奖励变量
            # 初始化奖励变量
            #reward = GetReward(graph=self.graph, multicast_tree = multicast_tree)
            rewardstep = GetReward(graph=graph, multicast_tree = multicast_tree)
            # 用于存储所有边的集合
            all_edges = set()
            # 迭代 multicast_tree 中的每条路径
            for path in multicast_tree:
                # 生成路径中的边
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                # 将边添加到集合中（自动去重）
                all_edges.update(edges)

            #Maxbw = GetMaxbw(self.graph)
            #Minbw = GetMinbw(graph)
            #Maxdelay = GetMaxdelay(graph)
            #Mindelay = GetMindelay(self.graph)
            #cost = 0

            #for edge in all_edges:
                #bandwidth = self.graph.edges[edge]['bw']
                #delay = self.graph.edges[edge]['delay']
                #cost += bandwidth / Maxbw + delay / Mindelay

            #cost = len(all_edges)
            #cost11 = len(all_edges)
            #rewardall = -cost11
            #reward = rewardstep*0.9 + rewardall*0.1

            reward = rewardstep

            # 设置 next_state
            if current_node == d1:
                next_node = d2
            elif current_node == d2:
                next_node = d3
            else:
                next_node = 11  # 如果 current_state 既不是 d1 也不是 d2
            next_state = _one_hot(sw_list, next_node - 1,
                                          graph.nodes,
                                          len(graph.nodes) + 1).to(device)
            replay_buffer.add(current_state, action, reward, next_state, done)
            current_node = next_node
            episode_return += reward
            step = step + 1
            if replay_buffer.size() > minimal_size:
                #print replay_buffer.size()
                #print "1111111111111111111111111111111111111111111111111111"
                b_s, b_a, b_r, b_ns, b_d = replay_buffer.sample(batch_size)
                transition_dict = {
                    'states': b_s,
                    'actions': b_a,
                    'next_states': b_ns,
                    'rewards': b_r,
                    'dones': b_d
                }
                # update agent
                agent.update(transition_dict)
        #print "zuboshu", multicast_tree
        # 计算重复边的次数
        repeated_edge_count = 0
        repeated_edge_count = count_repeated_edges(multicast_tree)
        repeated_list.append(repeated_edge_count)

        # # 计算时延带宽
        # delay = 0
        # delay = get_multicast_tree_delay(multicast_tree)
        # delay_list.append(delay)
        #
        #
        # bw = 0
        # bw = self.get_multicast_tree_bw(multicast_tree)
        # bw_list.append(bw)

        #share_file_path = "/home/sa/桌面/GaSteiner5/share.txt"
        #with open(share_file_path, "a") as file:
        #file.write("{}\n".format(repeated_edge_count))
        return_list.append(episode_return)

    # 保存 return_list 到文件
    result_file_path = "G:/rlcode/D3QN/resultD3QN_new/10/result.csv"
    # 假设 multicast_path 是你要保存的数据
    save_to_csv(result_file_path, return_list)



    # # 保存 return_list 到文件
    # result_file_path = "G:/rlcode/D3QN/result/result.csv"
    # with open(result_file_path, "w") as file:
    #     for episode_return in return_list:
    #         file.write("{}\n".format(episode_return))

    #print "Training completed and results are saved to:", result_file_path

    # 保存 repeated_list 到文件
    share_file_path = "G:/rlcode/D3QN/resultD3QN_new/10/share.csv"
    save_to_csv(share_file_path, repeated_list)



    # # 保存 return_list 到文件
    # share_file_path = "/home/sa/桌面/GaSteiner5/share.csv"
    # with open(share_file_path, "w") as file:
    #     for repeated_edge_count in repeated_list:
    #         file.write("{}\n".format(repeated_edge_count))

    # # 保存 return_list 到文件
    # bw_file_path = "/home/sa/桌面/GaSteiner5/bw.txt"
    # with open(bw_file_path, "w") as file:
    #     for bw in bw_list:
    #         file.write("{}\n".format(bw))
    #
    # # 保存 return_list 到文件
    # delay_file_path = "/home/sa/桌面/GaSteiner5/delay.txt"
    # with open(delay_file_path, "w") as file:
    #     for delay in delay_list:
    #         file.write("{}\n".format(delay))

    # episodes_list = list(range(len(return_list)))
    # plt.plot(episodes_list, return_list)
    # plt.xlabel('Episodes')
    # plt.ylabel('Returns')
    # plt.title('DQN learning')
    # plt.show()
    #
    # mv_return = rl_utils.moving_average(return_list, 27)
    # plt.plot(episodes_list, mv_return)
    # plt.xlabel('Episodes')
    # plt.ylabel('Returns')
    # plt.title('DQN learning')
    # plt.show()
    # print ("epsilon", epsilon)
    # print ("学习总次数", study_total)

    multicast_tree = []
    multicast_tree2 = []
    multicast_tree3 = []
    multicast_tree4 = []
    multicast_tree5 = []
    current_node = sw_list[1]
    while current_node != 11:
        with torch.no_grad():
            current_state = _one_hot(sw_list, current_node - 1,graph.nodes,len(graph.nodes) + 1).to(device)
            q_values = agent.q_net(current_state)
            # 打印调试信息
            #print("current_node:", current_node)
            #print("q_values:", q_values)
            # 去除第一维的单个维度，确保 q_values 是一维的
            q_values = q_values.squeeze(0)


            if current_node == sw_list[1]:
                action_range = q_values[0:k]
                offset = 0
            elif current_node == sw_list[2]:
                action_range = q_values[k:2 * k]
                offset = k
            elif current_node == sw_list[3]:
                action_range = q_values[2 * k:3 * k]
                offset = 2 * k
            # 获取动作范围内前五个最大的动作
            # 确保 action_range 是一个有效的张量或数组
            if isinstance(action_range, torch.Tensor):
                # 获取动作范围内前五个最大的动作
                top_actions = action_range.argsort(descending=True)[:5] + offset
            else:
                top_actions = np.argsort(action_range)[-5:][::-1] + offset






            # 根据current_state选择不同范围的动作
            # if current_node == sw_list[1]:
            #     action = q_values[0:k].argmax().item()
            # elif current_node == sw_list[2]:
            #     action = q_values[k:2*k].argmax().item() + k
            # elif current_node == sw_list[3]:
            #     action = q_values[2*k:3*k].argmax().item() + 2*k
            #max_action = q_values.argmax().item()  # 获取Q值最大的动作
            # print ("current_state", current_state)
            # print ("max_action:", action)
            # print ("path_indices[max_action]",path_indices[action])
            # 将 max_action 添加到 multicast_tree
            #multicast_tree.append(path_indices[action])


            for i, action in enumerate(top_actions):
                action_value = int(action.item())  # 将 action 的值转换为整数
                if action_value in path_indices:
                    if i == 0:
                        multicast_tree.append(path_indices[action_value])
                    elif i == 1:
                        multicast_tree2.append(path_indices[action_value])
                    elif i == 2:
                        multicast_tree3.append(path_indices[action_value])
                    elif i == 3:
                        multicast_tree4.append(path_indices[action_value])
                    elif i == 4:
                        multicast_tree5.append(path_indices[action_value])
                else:
                    print(f"Action {action_value} is not in path_indices")




        # 设置 next_state
        if current_node == sw_list[1]:
            next_node = sw_list[2]
        elif current_node == sw_list[2]:
            next_node = sw_list[3]
        else:
            next_node = 11  # 如果 current_state 既不是 d1 也不是 d2
        #print "current_node",current_node
        current_node = next_node
        #print "current_node",current_node

    # 将 multicast_tree 转换为使用小括号的元组
    multicast_path = tuple(tuple(path) for path in multicast_tree)
    multicast_path2 = tuple(tuple(path) for path in multicast_tree2)
    multicast_path3 = tuple(tuple(path) for path in multicast_tree3)
    multicast_path4 = tuple(tuple(path) for path in multicast_tree4)
    multicast_path5 = tuple(tuple(path) for path in multicast_tree5)
    print("最终路径:", multicast_path)
    print("最终路径:", multicast_path2)
    print("最终路径:", multicast_path3)
    print("最终路径:", multicast_path4)
    print("最终路径:", multicast_path5)
    # 保存 return_list 到文件
    path_file_path = "G:/rlcode/D3QN/resultD3QN_new/10/path.txt"
    path_file_path2 = "G:/rlcode/D3QN/resultD3QN_new/10/path2.txt"
    path_file_path3 = "G:/rlcode/D3QN/resultD3QN_new/10/path3.txt"
    path_file_path4 = "G:/rlcode/D3QN/resultD3QN_new/10/path4.txt"
    path_file_path5 = "G:/rlcode/D3QN/resultD3QN_new/10/path5.txt"
    with open(path_file_path, "a") as file:
        file.write("{}\n".format(multicast_path))
    with open(path_file_path2, "a") as file:
        file.write("{}\n".format(multicast_path2))
    with open(path_file_path3, "a") as file:
        file.write("{}\n".format(multicast_path3))
    with open(path_file_path4, "a") as file:
        file.write("{}\n".format(multicast_path4))
    with open(path_file_path5, "a") as file:
        file.write("{}\n".format(multicast_path5))
    # 将 multicast_tree 转换为使用小括号的元组
    # multicast_path = tuple(tuple(path) for path in multicast_tree)
    # print ("最终路径:", multicast_path)
    # # 保存 return_list 到文件
    # path_file_path = "G:/rlcode/D3QN/resultD3QN_new/10/path.txt"
    #
    # with open(path_file_path, "a") as file:
    #     file.write("{}\n".format(multicast_path))
    #
    # #print "Training completed and results are saved to:", path_file_path
    return multicast_path





# 按文件名中的第一个"-"前的数字排序
def sort_files_by_number(files):
    return sorted(files, key=lambda x: int(x.split('-')[0]))


# 遍历前60个pkl文件并计算所需信息
def process_first_60_pickles(folder_path, num_destinations,src_sw, dst_sw1):
    results = []

    files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]
    sorted_files = sort_files_by_number(files)[:120]

    for filename in sorted_files:
        file_path = os.path.join(folder_path, filename)
        graph = read_pickle(file_path)
        sw_list = get_sw_list(graph, num_destinations, src_sw, dst_sw1)


        multicast_path = D3QN(graph, sw_list)
        paths_info = calculate_paths_info(graph, multicast_path)


        delays = [info[0] for info in paths_info]
        total_losses = [info[1] for info in paths_info]
        min_bws = [info[2] for info in paths_info]

        max_delay = max(delays)
        total_loss = sum(total_losses)
        min_bw = min(min_bws)

        results.append({
            'file': filename,
            'multicast_path': multicast_path,
            'max_delay': max_delay,
            'total_loss': total_loss,
            'min_bw': min_bw
        })

    return results


if __name__ == '__main__':
    folder_path = 'G:/rlcode/D3QN/Experimental Dataset/node10_data'
    num_destinations = 3  # 目的节点的数量
    src_sw = 2
    dst_sw1 = 3
    results = process_first_60_pickles(folder_path, num_destinations,src_sw, dst_sw1)

    for result in results:
        print(f"文件: {result['file']}")
        for i, path in enumerate(result['multicast_path']):
            if path is not None:
                print(f"路径 {i + 1}: {path}")
            else:
                print(f"路径 {i + 1}: 没有找到路径")
        print(f"三条路径中时延最大的一条路径的时延: {result['max_delay']}")
        print(f"三条路径中所有节点中两两之间最小的带宽的值: {result['min_bw']}")
        print(f"三条路径中所有的丢包率之和: {result['total_loss']}")
        print("----------------------------")




