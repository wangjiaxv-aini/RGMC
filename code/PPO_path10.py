# -*- coding:utf-8 -*-

import numpy as np
import torch
import matplotlib.pyplot as plt
import PPO_tools
from getreward import GetReward
from getreward import GetMinbw
from getreward import GetMaxdelay
from getreward import GetMaxloss
import networkx as nx
import random
import csv
import os


def save_to_csv(file_path, data_list):
    """Save data to CSV file"""
    existing_data = []
    try:
        with open(file_path, "r", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                existing_data.append(row)
    except FileNotFoundError:
        existing_data = []

    for i, data in enumerate(data_list):
        if i < len(existing_data):
            existing_data[i].append(data)
        else:
            existing_data.append([data])

    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)


def read_pickle(pickle_path):
    """Read network topology from pickle file"""
    return nx.read_gpickle(pickle_path)


def get_sw_list(graph, num_destinations, src_sw, dst_sw1):
    """Get source and destination nodes"""
    sw_list = [src_sw, dst_sw1]
    for i in range(1, num_destinations):
        sw_next = (dst_sw1 + 3 * i) % 10
        if sw_next == 0:
            sw_next = 10
        sw_list.append(sw_next)
    return sw_list


def get_path_info(graph, path):
    """Calculate path information (delay, loss, bandwidth)"""
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
    """Count repeated edges in multicast tree"""
    edge_counts = {}

    for path in multicast_tree:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge in edge_counts:
                edge_counts[edge] += 1
            else:
                edge_counts[edge] = 1

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
    """Select k candidate paths for each destination"""
    src = sw_list[0]
    d1, d2, d3 = sw_list[1], sw_list[2], sw_list[3]
    paths_to_all = []
    paths_to_d1 = []
    paths_to_d2 = []
    paths_to_d3 = []

    min_bw = GetMinbw(graph)
    max_delay = GetMaxdelay(graph)
    max_loss = GetMaxloss(graph)

    def path_weight(path):
        weight = 0
        for i in range(len(path) - 1):
            edge_data = graph[path[i]][path[i + 1]]
            if edge_data['bw'] == 0:
                norm_bw = 1
            else:
                norm_bw = min_bw / edge_data['bw']
            norm_delay = edge_data['delay'] / max_delay
            norm_loss = edge_data['loss'] / max_loss
            weight += norm_bw + norm_delay + norm_loss
        return weight

    def get_k_paths(all_paths, k):
        all_paths.sort(key=path_weight)
        if len(all_paths) >= k:
            return all_paths[:k]
        else:
            extended_paths = all_paths * (k // len(all_paths)) + all_paths[:k % len(all_paths)]
            return extended_paths[:k]

    for target_node in [d1, d2, d3]:
        all_paths = list(nx.all_simple_paths(graph, src, target_node))
        if target_node == d1:
            paths_to_d1.extend(all_paths)
        elif target_node == d2:
            paths_to_d2.extend(all_paths)
        elif target_node == d3:
            paths_to_d3.extend(all_paths)

    paths_to_all.extend(get_k_paths(paths_to_d1, k))
    paths_to_all.extend(get_k_paths(paths_to_d2, k))
    paths_to_all.extend(get_k_paths(paths_to_d3, k))
    path_indices = {i: paths_to_all[i] for i in range(len(paths_to_all))}

    return paths_to_all, paths_to_d1, paths_to_d2, paths_to_d3, path_indices


def calculate_paths_info(graph, multicast_path):
    """Calculate information for all paths in multicast tree"""
    paths_info = []
    for path in multicast_path:
        try:
            delay, loss, min_bw = get_path_info(graph, path)
            paths_info.append((delay, loss, min_bw))
        except nx.NetworkXNoPath:
            paths_info.append((float('inf'), float('inf'), float('inf')))
    return paths_info


def PPO_multicast(graph, sw_list):
    """Main PPO algorithm for multicast tree construction"""
    print("进来了")
    print("sw_list", sw_list)

    print("Number of nodes:", graph.number_of_nodes())
    print("Number of edges:", graph.number_of_edges())

    # Hyperparameters
    src = sw_list[0]
    d1, d2, d3 = sw_list[1:]

    actor_lr = 3e-4
    critic_lr = 1e-3
    num_episodes = 500
    hidden_dim = 128
    gamma = 0.9
    lmbda = 0.95  # GAE lambda
    epochs = 10  # PPO update epochs
    eps_clip = 0.2  # PPO clip parameter
    k = 30  # Number of candidate paths
    update_frequency = 10  # Update every N episodes

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)

    # Get candidate paths
    paths_to_all, paths_to_d1, paths_to_d2, paths_to_d3, path_indices = select_k_paths(
        graph=graph, sw_list=sw_list, k=k)

    state_dim = len(graph.nodes) + 1
    action_dim = len(paths_to_all)

    # Initialize PPO agent
    agent = PPO_tools.PPO(state_dim, hidden_dim, action_dim, actor_lr, critic_lr,
                          gamma, lmbda, epochs, eps_clip, device)

    # Initialize trajectory buffer
    trajectory_buffer = PPO_tools.TrajectoryBuffer()

    return_list = []
    repeated_list = []

    for episode in range(15000):
        episode_return = 0
        multicast_tree = []
        current_node = d1
        done = False

        while not done:
            if current_node == 11:
                done = True
                break

            # Get current state
            current_state = _one_hot(sw_list, current_node - 1, graph.nodes,
                                     len(graph.nodes) + 1).cpu().numpy()

            # Determine action range based on current node
            if current_node == sw_list[1]:
                k_range = (0, k)
            elif current_node == sw_list[2]:
                k_range = (k, 2 * k)
            elif current_node == sw_list[3]:
                k_range = (2 * k, 3 * k)
            else:
                k_range = None

            # Select action using PPO policy
            action, log_prob = agent.take_action(current_state, k_range)

            # Add selected path to multicast tree
            multicast_tree.append(path_indices[action])

            # Calculate reward
            reward = GetReward(graph=graph, multicast_tree=multicast_tree)

            # Determine next state
            if current_node == d1:
                next_node = d2
            elif current_node == d2:
                next_node = d3
            else:
                next_node = 11

            next_state = _one_hot(sw_list, next_node - 1, graph.nodes,
                                  len(graph.nodes) + 1).cpu().numpy()

            # Store transition
            trajectory_buffer.add(current_state, action, reward, next_state, done, log_prob)

            current_node = next_node
            episode_return += reward

        # Count repeated edges
        repeated_edge_count = count_repeated_edges(multicast_tree)
        repeated_list.append(repeated_edge_count)
        return_list.append(episode_return)

        # Update policy every update_frequency episodes
        if (episode + 1) % update_frequency == 0 and trajectory_buffer.size() > 0:
            agent.update(trajectory_buffer)
            trajectory_buffer.clear()

    # Save results
    result_file_path = "E:\学术12.16\code\D3QN/resultPPO/10/result.csv"
    save_to_csv(result_file_path, return_list)

    share_file_path = "E:\学术12.16\code\D3QN/resultPPO/10/share.csv"
    save_to_csv(share_file_path, repeated_list)

    # Generate final multicast tree using trained policy
    multicast_tree = []
    multicast_tree2 = []
    multicast_tree3 = []
    multicast_tree4 = []
    multicast_tree5 = []
    current_node = sw_list[1]

    while current_node != 11:
        with torch.no_grad():
            current_state = _one_hot(sw_list, current_node - 1, graph.nodes,
                                     len(graph.nodes) + 1).cpu().numpy()
            current_state_tensor = torch.tensor(current_state, dtype=torch.float).to(device)
            probs = agent.actor(current_state_tensor).cpu().numpy()

            # Get top 5 actions for each destination
            if current_node == sw_list[1]:
                action_probs = probs[0:k]
                offset = 0
            elif current_node == sw_list[2]:
                action_probs = probs[k:2 * k]
                offset = k
            elif current_node == sw_list[3]:
                action_probs = probs[2 * k:3 * k]
                offset = 2 * k

            top_actions = np.argsort(action_probs)[-5:][::-1] + offset

            for i, action in enumerate(top_actions):
                if action in path_indices:
                    if i == 0:
                        multicast_tree.append(path_indices[action])
                    elif i == 1:
                        multicast_tree2.append(path_indices[action])
                    elif i == 2:
                        multicast_tree3.append(path_indices[action])
                    elif i == 3:
                        multicast_tree4.append(path_indices[action])
                    elif i == 4:
                        multicast_tree5.append(path_indices[action])

        if current_node == sw_list[1]:
            next_node = sw_list[2]
        elif current_node == sw_list[2]:
            next_node = sw_list[3]
        else:
            next_node = 11
        current_node = next_node

    # Convert to tuples
    multicast_path = tuple(tuple(path) for path in multicast_tree)
    multicast_path2 = tuple(tuple(path) for path in multicast_tree2)
    multicast_path3 = tuple(tuple(path) for path in multicast_tree3)
    multicast_path4 = tuple(tuple(path) for path in multicast_tree4)
    multicast_path5 = tuple(tuple(path) for path in multicast_tree5)

    print("最终路径:", multicast_path)
    print("最终路径2:", multicast_path2)
    print("最终路径3:", multicast_path3)
    print("最终路径4:", multicast_path4)
    print("最终路径5:", multicast_path5)

    # Save paths
    path_file_path = "E:\学术12.16\code\D3QN/resultPPO/10/path.txt"
    path_file_path2 = "E:\学术12.16\code\D3QN/resultPPO/10/path2.txt"
    path_file_path3 = "E:\学术12.16\code\D3QN/resultPPO/10/path3.txt"
    path_file_path4 = "E:\学术12.16\code\D3QN/resultPPO/10/path4.txt"
    path_file_path5 = "E:\学术12.16\code\D3QN/resultPPO/10/path5.txt"

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

    return multicast_path


def sort_files_by_number(files):
    """Sort files by number in filename"""
    return sorted(files, key=lambda x: int(x.split('-')[0]))


def process_first_60_pickles(folder_path, num_destinations, src_sw, dst_sw1):
    """Process first 60 pickle files"""
    results = []

    files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]
    sorted_files = sort_files_by_number(files)[:120]

    for filename in sorted_files:
        file_path = os.path.join(folder_path, filename)
        graph = read_pickle(file_path)
        sw_list = get_sw_list(graph, num_destinations, src_sw, dst_sw1)

        multicast_path = PPO_multicast(graph, sw_list)
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
    folder_path = 'E:\学术12.16\code\D3QN\Experimental Dataset/node10_data'
    num_destinations = 3
    src_sw = 2
    dst_sw1 = 3
    results = process_first_60_pickles(folder_path, num_destinations, src_sw, dst_sw1)

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
