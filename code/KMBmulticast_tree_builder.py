# -*- coding: utf-8 -*-
import os
import networkx as nx
from networkx.algorithms.approximation import steiner_tree
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import namedtuple
import pandas as pd

# 定义路由参数结构
RouteParams = namedtuple("RouteParams", ('bw', 'delay', 'loss', 'length'))

class MulticastTreeBuilder:
    """组播树构建器，基于KMB算法"""
    
    def __init__(self):
        self.results = []  # 存储所有文件的计算结果
    
    def read_pickle_graph(self, pickle_path):
        """读取pickle文件中的网络图"""
        try:
            pkl_graph = nx.read_gpickle(pickle_path)
            return pkl_graph
        except Exception as e:
            print(f"读取文件 {pickle_path} 失败: {e}")
            return None
    
    def modify_bw_weight(self, graph):
        """将带宽权重取倒数，用于最大化带宽优化"""
        _g = graph.copy()
        for edge in graph.edges():
            bw = graph[edge[0]][edge[1]]['bw']
            # 避免除零错误，对于带宽为0的边设置很大的权重
            if bw <= 0:
                _g[edge[0]][edge[1]]['bw_weight'] = 1000000
            else:
                _g[edge[0]][edge[1]]['bw_weight'] = 1.0 / bw
        return _g
    
    def kmb_algorithm(self, graph, src_node, dst_nodes, weight=None):
        """KMB算法实现 - 构建Steiner树"""
        try:
            terminals = [src_node] + dst_nodes
            # 确保所有终端节点都在图中
            for node in terminals:
                if node not in graph.nodes():
                    print(f"警告: 节点 {node} 不在图中")
                    return None
            
            st_tree = steiner_tree(graph, terminals, weight)
            return st_tree
        except Exception as e:
            print(f"KMB算法执行失败: {e}")
            return None
    
    def calculate_end_to_end_bandwidth(self, tree, src_node, dst_nodes):
        """计算端到端最小带宽"""
        min_bandwidths = []
        
        for dst in dst_nodes:
            try:
                # 寻找从源到目标的路径
                path = nx.shortest_path(tree, src_node, dst)
                if len(path) < 2:
                    min_bandwidths.append(float('inf'))
                    continue
                
                # 计算路径上的最小带宽
                min_bw = float('inf')
                for i in range(len(path) - 1):
                    edge_bw = tree[path[i]][path[i+1]]['bw']
                    min_bw = min(min_bw, edge_bw)
                
                min_bandwidths.append(min_bw)
            except nx.NetworkXNoPath:
                print(f"警告: 从节点{src_node}到节点{dst}没有路径")
                min_bandwidths.append(0)
        
        return min_bandwidths
    
    def get_tree_params(self, tree, graph, src_node, dst_nodes):
        """计算树的各项网络参数"""
        if tree is None or len(tree.edges()) == 0:
            return RouteParams(0, 0, 0, 0)
        
        # 计算总和参数
        total_bw, total_delay, total_loss = 0, 0, 0
        edge_count = 0
        
        for edge in tree.edges():
            total_bw += graph[edge[0]][edge[1]]['bw']
            total_delay += graph[edge[0]][edge[1]]['delay']
            total_loss += graph[edge[0]][edge[1]]['loss']
            edge_count += 1
        
        # 计算端到端最小带宽的平均值
        min_bandwidths = self.calculate_end_to_end_bandwidth(tree, src_node, dst_nodes)
        avg_min_bw = np.mean([bw for bw in min_bandwidths if bw != float('inf')])
        
        # 返回参数：平均最小带宽、平均延迟、平均丢包率、边数
        if edge_count > 0:
            return RouteParams(
                avg_min_bw,
                total_delay / edge_count,
                total_loss / edge_count,
                edge_count
            )
        else:
            return RouteParams(0, 0, 0, 0)
    
    def build_multicast_trees(self, graph, src_node, dst_nodes):
        """构建多种优化目标的组播树"""
        results = {}
        
        # 1. 优化带宽的树 (最大化带宽)
        bw_graph = self.modify_bw_weight(graph)
        bw_tree = self.kmb_algorithm(bw_graph, src_node, dst_nodes, weight='bw_weight')
        results['bandwidth_optimized'] = {
            'tree': bw_tree,
            'params': self.get_tree_params(bw_tree, graph, src_node, dst_nodes) if bw_tree else None,
            'description': '带宽优化组播树'
        }
        
        # 2. 优化延迟的树 (最小化延迟)
        delay_tree = self.kmb_algorithm(graph, src_node, dst_nodes, weight='delay')
        results['delay_optimized'] = {
            'tree': delay_tree,
            'params': self.get_tree_params(delay_tree, graph, src_node, dst_nodes) if delay_tree else None,
            'description': '延迟优化组播树'
        }
        
        # 3. 优化丢包率的树 (最小化丢包率)
        loss_tree = self.kmb_algorithm(graph, src_node, dst_nodes, weight='loss')
        results['loss_optimized'] = {
            'tree': loss_tree,
            'params': self.get_tree_params(loss_tree, graph, src_node, dst_nodes) if loss_tree else None,
            'description': '丢包率优化组播树'
        }
        
        # 4. 跳数优化的树 (最小化跳数)
        hop_tree = self.kmb_algorithm(graph, src_node, dst_nodes, weight=None)
        results['hop_optimized'] = {
            'tree': hop_tree,
            'params': self.get_tree_params(hop_tree, graph, src_node, dst_nodes) if hop_tree else None,
            'description': '跳数优化组播树'
        }
        
        return results
    
    def visualize_tree(self, graph, tree, src_node, dst_nodes, title="组播树"):
        """可视化组播树"""
        plt.figure(figsize=(12, 8))
        
        # 设置节点位置
        pos = nx.spring_layout(graph, seed=42)
        
        # 绘制原始图的所有边（灰色）
        nx.draw_networkx_edges(graph, pos, edge_color='lightgray', alpha=0.3)
        
        # 绘制树的边（红色）
        if tree and len(tree.edges()) > 0:
            nx.draw_networkx_edges(tree, pos, edge_color='red', width=2)
        
        # 绘制所有节点
        node_colors = []
        for node in graph.nodes():
            if node == src_node:
                node_colors.append('green')  # 源节点
            elif node in dst_nodes:
                node_colors.append('blue')   # 目标节点
            else:
                node_colors.append('lightblue')  # 普通节点
        
        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_labels(graph, pos)
        
        plt.title(title)
        plt.legend(['源节点(绿)', '目标节点(蓝)', '组播树边(红)', '其他边(灰)'])
        plt.axis('off')
        plt.tight_layout()
        return plt
    
    def process_single_file(self, file_path, src_node, dst_nodes):
        """处理单个pkl文件"""
        print(f"\n处理文件: {file_path}")
        
        # 读取图数据
        graph = self.read_pickle_graph(file_path)
        if graph is None:
            return None
        
        print(f"图信息: {len(graph.nodes())}个节点, {len(graph.edges())}条边")
        print(f"源节点: {src_node}, 目标节点: {dst_nodes}")
        
        # 构建组播树
        results = self.build_multicast_trees(graph, src_node, dst_nodes)
        
        # 打印结果
        print("\n=== 组播树构建结果 ===")
        for opt_type, result in results.items():
            tree = result['tree']
            params = result['params']
            desc = result['description']
            
            print(f"\n{desc}:")
            if tree and params:
                print(f"  平均最小带宽: {params.bw:.2f}")
                print(f"  平均延迟: {params.delay:.2f}")
                print(f"  平均丢包率: {params.loss:.6f}")
                print(f"  边数: {params.length}")
                print(f"  树的边: {list(tree.edges())}")
            else:
                print("  构建失败")
        
        return {
            'file': os.path.basename(file_path),
            'graph': graph,
            'results': results
        }
    
    def process_all_files(self, data_dir, src_node, dst_nodes, max_files=10):
        """处理目录中的所有pkl文件"""
        data_path = Path(data_dir)
        pkl_files = sorted([f for f in data_path.glob('*.pkl')], 
                          key=lambda x: int(x.stem.split('-')[0]))
        
        print(f"发现 {len(pkl_files)} 个pkl文件")
        
        # 限制处理的文件数量
        files_to_process = pkl_files[:max_files]
        print(f"将处理前 {len(files_to_process)} 个文件")
        
        summary_data = []
        
        for file_path in files_to_process:
            result = self.process_single_file(file_path, src_node, dst_nodes)
            if result:
                self.results.append(result)
                
                # 收集汇总数据
                for opt_type, opt_result in result['results'].items():
                    if opt_result['params']:
                        summary_data.append({
                            'file': result['file'],
                            'optimization': opt_type,
                            'avg_min_bandwidth': opt_result['params'].bw,
                            'avg_delay': opt_result['params'].delay,
                            'avg_loss': opt_result['params'].loss,
                            'edges': opt_result['params'].length
                        })
        
        # 创建汇总表
        if summary_data:
            df = pd.DataFrame(summary_data)
            print("\n=== 汇总统计 ===")
            print(df.groupby('optimization').agg({
                'avg_min_bandwidth': ['mean', 'std'],
                'avg_delay': ['mean', 'std'],
                'avg_loss': ['mean', 'std'],
                'edges': ['mean', 'std']
            }).round(4))
            
            return df
        
        return None
    
    def save_visualization(self, file_index=0, save_path='/mnt/user-data/outputs/'):
        """保存可视化结果"""
        if not self.results or file_index >= len(self.results):
            print("没有可用的结果进行可视化")
            return
        
        result = self.results[file_index]
        graph = result['graph']
        
        # 获取参数
        src_node = 2
        dst_nodes = [4, 6, 8]
        
        # 为每种优化方法创建可视化
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        for i, (opt_type, opt_result) in enumerate(result['results'].items()):
            if i < 4 and opt_result['tree']:
                plt.sca(axes[i])
                
                # 设置节点位置
                pos = nx.spring_layout(graph, seed=42)
                
                # 绘制原始图的所有边（灰色）
                nx.draw_networkx_edges(graph, pos, edge_color='lightgray', alpha=0.3)
                
                # 绘制树的边（红色）
                nx.draw_networkx_edges(opt_result['tree'], pos, edge_color='red', width=2)
                
                # 绘制节点
                node_colors = []
                for node in graph.nodes():
                    if node == src_node:
                        node_colors.append('green')
                    elif node in dst_nodes:
                        node_colors.append('blue')
                    else:
                        node_colors.append('lightblue')
                
                nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=300)
                nx.draw_networkx_labels(graph, pos, font_size=8)
                
                # 添加参数信息到标题
                params = opt_result['params']
                title = f"{opt_result['description']}\n"
                title += f"带宽:{params.bw:.1f} 延迟:{params.delay:.1f}\n"
                title += f"丢包率:{params.loss:.3f} 边数:{params.length}"
                
                plt.title(title, fontsize=10)
                plt.axis('off')
        
        plt.suptitle(f"组播树对比 - 文件: {result['file']}\n源节点: {src_node}, 目标节点: {dst_nodes}", 
                    fontsize=14)
        plt.tight_layout()
        
        # 保存图片
        save_file = Path(save_path) / f"multicast_trees_{result['file'].replace('.pkl', '.png')}"
        plt.savefig(save_file, dpi=300, bbox_inches='tight')
        print(f"可视化结果已保存到: {save_file}")
        plt.show()

def main():
    # 配置参数
    data_directory = r"E:\学术12.16\code\D3QN\Experimental Dataset\node14_data"
    source_node = 2
    destination_nodes = [4, 6, 8]
    max_files_to_process = 5  # 限制处理文件数量，避免运行时间过长
    
    # 创建组播树构建器
    builder = MulticastTreeBuilder()
    
    # 处理所有文件
    print("开始处理pkl文件...")
    summary_df = builder.process_all_files(data_directory, source_node, destination_nodes, max_files_to_process)
    
    # 保存汇总结果
    if summary_df is not None:
        summary_file = "/mnt/user-data/outputs/multicast_summary.csv"
        summary_df.to_csv(summary_file, index=False)
        print(f"\n汇总结果已保存到: {summary_file}")
    
    # 保存第一个文件的可视化结果
    if builder.results:
        builder.save_visualization(0)
    
    print("\n处理完成！")

if __name__ == '__main__':
    main()
