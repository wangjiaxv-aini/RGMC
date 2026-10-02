#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
SCTF算法批量处理脚本（分组统计版）
源节点：2
目的节点：4, 6, 8
每30个文件为一组进行统计
"""
import os
import pickle
import numpy as np
import networkx as nx
import copy
import random


class Data_process:
    """数据预处理类：归一化和加权"""

    def __init__(self, graph):
        self.graph = graph
        self.attributes = set()
        self.attr_value_dict = {}
        self.new_graph = copy.deepcopy(self.graph)
        self.epsilon = 1e-6

        for u, v, data in self.graph.edges(data=True):
            self.attributes.update(data.keys())

    def normalization(self):
        """图属性归一化到[0,1]"""
        for attr in self.attributes:
            attr_value_list = list(nx.get_edge_attributes(self.graph, attr).values())
            attr_value_max = max(attr_value_list)
            attr_value_min = min(attr_value_list)
            for u, v in self.graph.edges:
                attr_value = self.graph[u][v][attr]
                self.new_graph[u][v][attr] = (attr_value - attr_value_min) / (
                        attr_value_max - attr_value_min + self.epsilon)
        return self.new_graph

    def weight(self, beta, negative_attr):
        """生成加权属性"""
        if 'weight' in self.attributes:
            print("attribute 'weight' has been exiting")
        else:
            self.new_graph = self.normalization()
            attr_list = sorted(self.attributes)
            for u, v in self.graph.edges:
                weight = 0.
                for attr_value, beta_value, neg_flag in zip(attr_list, beta, negative_attr):
                    weight += self.new_graph[u][v][attr_value] * (neg_flag == 0) * beta_value \
                              + (1 - self.new_graph[u][v][attr_value]) * (neg_flag == 1) * beta_value
                self.new_graph[u][v]['weight'] = weight
        return self.new_graph


class SCTF:
    """SCTF算法实现"""

    def __init__(self, graph, src, stds):
        self.topo = copy.deepcopy(graph)
        self.src = src
        self.stds = copy.deepcopy(stds)
        self.result = {}

    def step(self):
        """一步迭代：选择一个目的节点，计算最短路径，将路径权重设为0"""
        std = random.choice(self.stds)
        self.stds.remove(std)
        shortest_path = nx.shortest_path(self.topo, self.src, std, weight='weight')
        self.result[(self.src, std)] = shortest_path
        for i, node in enumerate(shortest_path):
            if i > 0:
                self.topo[shortest_path[i - 1]][node]['weight'] = 0

    def run(self):
        """运行完整算法"""
        while len(self.stds) > 0:
            self.step()
        return self.result


def generating_tree(paths):
    """从路径生成组播树"""
    new_graph = nx.DiGraph()
    link_set = set()
    for path in paths.values():
        for i in range(len(path)):
            if i > 0 and path[i - 1] != path[i] and (path[i - 1], path[i]) not in link_set \
                    and (path[i], path[i - 1]) not in link_set:
                new_graph.add_edge(path[i - 1], path[i])
                link_set.update([(path[i - 1], path[i])])
    return new_graph


def tree_evaluate(graph, tree, paths):
    """评估组播树性能指标"""
    bottleneck_bw_list = []
    path_delay_list = []

    for node_list in paths.values():
        bw0 = float('inf')
        path_delay = 0

        for i, node in enumerate(node_list):
            if i > 0 and node_list[i - 1] != node:
                bottleneck_bw = min(bw0, graph[node_list[i - 1]][node]['bw'])
                bw0 = bottleneck_bw
                path_delay += graph[node_list[i - 1]][node]['delay']

        bottleneck_bw_list.append(bw0)
        path_delay_list.append(path_delay)

    # 计算组播树所有链路的丢包率之和
    loss_sum = 0
    for u, v in tree.edges:
        if u != v:
            loss_sum += graph[u][v]['loss']

    bottleneck_bw_mean = np.mean(bottleneck_bw_list)
    tree_len = len(tree.edges)
    max_path_delay = max(path_delay_list) if path_delay_list else 0

    return bottleneck_bw_mean, max_path_delay, loss_sum, tree_len, path_delay_list


def sort_files_by_number(file_list):
    """按照文件名第一个数字排序"""

    def get_first_number(filename):
        num_str = filename.split('-')[0]
        try:
            return int(num_str)
        except:
            return 0

    return sorted(file_list, key=get_first_number)


if __name__ == '__main__':
    # ==================== 参数设置 ====================
    directory_path = r'E:\学术12.16\code\D3QN\Experimental Dataset\Del'

    src = 2
    stds = [4, 6, 8]

    beta = [0.1, 0.6, 0.3]
    negative_attr = [1, 0, 0]

    GROUP_SIZE = 30  # 每组文件数量

    # ==================== 获取并排序文件 ====================
    file_list = os.listdir(directory_path)
    pkl_files = [f for f in file_list if f.endswith('.pkl')]
    sorted_files = sort_files_by_number(pkl_files)

    print("=" * 80)
    print(f"SCTF组播树计算（分组统计版）")
    print(f"源节点: {src}")
    print(f"目的节点: {stds}")
    print(f"数据路径: {directory_path}")
    print(f"文件总数: {len(sorted_files)}")
    print(f"分组大小: 每{GROUP_SIZE}个文件一组")
    print(f"权重配置: beta={beta}, negative_attr={negative_attr}")
    print("=" * 80)
    print()

    # 用于统计
    all_results = []
    group_results = []  # 存储每组的统计结果

    # ==================== 批量处理文件 ====================
    for index, file_name in enumerate(sorted_files, 1):
        try:
            file_path = os.path.join(directory_path, file_name)

            with open(file_path, 'rb') as pkl_file:
                graph = pickle.load(pkl_file)

            data_process = Data_process(graph)
            new_graph = data_process.weight(beta, negative_attr)

            model = SCTF(new_graph, src, stds)
            paths = model.run()

            tree = generating_tree(paths)

            result = tree_evaluate(graph, tree, paths)
            bottleneck_bw_mean, max_path_delay, loss_sum, tree_len, path_delay_list = result

            all_results.append({
                'file': file_name,
                'bottleneck_bw': bottleneck_bw_mean,
                'max_delay': max_path_delay,
                'loss_sum': loss_sum,
                'tree_len': tree_len,
                'path_delays': path_delay_list
            })

            print(f"[{index:3d}/{len(sorted_files)}] {file_name}")
            print(f"  各路径时延: {[f'{d:.4f}' for d in path_delay_list]}")
            print(f"  最大路径时延: {max_path_delay:.4f}")
            print(f"  瓶颈带宽均值: {bottleneck_bw_mean:.4f}")
            print(f"  组播树丢包率之和: {loss_sum:.6f}")
            print(f"  组播树边数: {tree_len}")

            # 每30个文件输出一次分组统计
            if index % GROUP_SIZE == 0 or index == len(sorted_files):
                group_start = ((index - 1) // GROUP_SIZE) * GROUP_SIZE + 1
                group_end = index
                group_data = all_results[group_start - 1:group_end]

                avg_bw = np.mean([r['bottleneck_bw'] for r in group_data])
                avg_max_delay = np.mean([r['max_delay'] for r in group_data])
                avg_loss_sum = np.mean([r['loss_sum'] for r in group_data])
                avg_tree_len = np.mean([r['tree_len'] for r in group_data])

                group_results.append({
                    'group': f"第{len(group_results) + 1}组 (文件{group_start}-{group_end})",
                    'file_range': (group_start, group_end),
                    'count': len(group_data),
                    'avg_bw': avg_bw,
                    'avg_max_delay': avg_max_delay,
                    'avg_loss_sum': avg_loss_sum,
                    'avg_tree_len': avg_tree_len
                })

                print("\n" + ">" * 80)
                print(f"【分组统计】第{len(group_results)}组 (文件 {group_start}-{group_end}, 共{len(group_data)}个)")
                print(f"  平均瓶颈带宽: {avg_bw:.4f}")
                print(f"  平均最大路径时延: {avg_max_delay:.4f}")
                print(f"  平均丢包率之和: {avg_loss_sum:.6f}")
                print(f"  平均树边数: {avg_tree_len:.2f}")
                print(">" * 80 + "\n")

            print("-" * 80)

        except Exception as e:
            print(f"[{index:3d}/{len(sorted_files)}] {file_name} - 处理失败: {str(e)}")
            print("-" * 80)

    # ==================== 最终统计汇总 ====================
    print("\n" + "=" * 80)
    print("各组统计结果汇总")
    print("=" * 80)

    if group_results:
        for i, group in enumerate(group_results, 1):
            print(f"\n{group['group']} ({group['count']}个文件)")
            print(f"  平均瓶颈带宽: {group['avg_bw']:.4f}")
            print(f"  平均最大路径时延: {group['avg_max_delay']:.4f}")
            print(f"  平均丢包率之和: {group['avg_loss_sum']:.6f}")
            print(f"  平均树边数: {group['avg_tree_len']:.2f}")

    print("\n" + "=" * 80)
    print("总体统计")
    print("=" * 80)

    if all_results:
        avg_bw = np.mean([r['bottleneck_bw'] for r in all_results])
        avg_max_delay = np.mean([r['max_delay'] for r in all_results])
        avg_loss_sum = np.mean([r['loss_sum'] for r in all_results])
        avg_tree_len = np.mean([r['tree_len'] for r in all_results])

        print(f"成功处理文件数: {len(all_results)}/{len(sorted_files)}")
        print(f"总分组数: {len(group_results)}")
        print(f"\n全部文件平均性能指标:")
        print(f"  平均瓶颈带宽: {avg_bw:.4f}")
        print(f"  平均最大路径时延: {avg_max_delay:.4f}")
        print(f"  平均丢包率之和: {avg_loss_sum:.6f}")
        print(f"  平均树边数: {avg_tree_len:.2f}")

    print("=" * 80)
    print("处理完成！")