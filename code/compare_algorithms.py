# -*- coding:utf-8 -*-
"""
Comparison script for D3QN vs PPO on multicast tree construction
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# Import both algorithms
import D3QN_path
import PPO_path


def compare_algorithms(folder_path, num_destinations, src_sw, dst_sw1, num_files=10):
    """
    Compare D3QN and PPO algorithms on the same network topologies
    
    Args:
        folder_path: Path to folder containing network topology files
        num_destinations: Number of destination nodes
        src_sw: Source switch
        dst_sw1: First destination switch
        num_files: Number of topology files to test
    """
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]
    sorted_files = sorted(files, key=lambda x: int(x.split('-')[0]))[:num_files]
    
    d3qn_results = []
    ppo_results = []
    
    print("="*60)
    print("Starting Algorithm Comparison")
    print("="*60)
    
    for idx, filename in enumerate(sorted_files):
        print(f"\nProcessing topology {idx+1}/{num_files}: {filename}")
        file_path = os.path.join(folder_path, filename)
        graph = D3QN_path.read_pickle(file_path)
        sw_list = D3QN_path.get_sw_list(graph, num_destinations, src_sw, dst_sw1)
        
        # Run D3QN
        print("  Running D3QN...")
        d3qn_path = D3QN_path.D3QN(graph, sw_list)
        d3qn_info = D3QN_path.calculate_paths_info(graph, d3qn_path)
        d3qn_results.append({
            'file': filename,
            'paths': d3qn_path,
            'max_delay': max([info[0] for info in d3qn_info]),
            'total_loss': sum([info[1] for info in d3qn_info]),
            'min_bw': min([info[2] for info in d3qn_info]),
            'repeated_edges': D3QN_path.count_repeated_edges(d3qn_path)
        })
        
        # Run PPO
        print("  Running PPO...")
        ppo_path = PPO_path.PPO_multicast(graph, sw_list)
        ppo_info = PPO_path.calculate_paths_info(graph, ppo_path)
        ppo_results.append({
            'file': filename,
            'paths': ppo_path,
            'max_delay': max([info[0] for info in ppo_info]),
            'total_loss': sum([info[1] for info in ppo_info]),
            'min_bw': min([info[2] for info in ppo_info]),
            'repeated_edges': PPO_path.count_repeated_edges(ppo_path)
        })
    
    # Print comparison results
    print("\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    
    print("\n{:<30} {:<15} {:<15}".format("Metric", "D3QN", "PPO"))
    print("-"*60)
    
    # Average max delay
    avg_d3qn_delay = np.mean([r['max_delay'] for r in d3qn_results])
    avg_ppo_delay = np.mean([r['max_delay'] for r in ppo_results])
    print("{:<30} {:<15.4f} {:<15.4f}".format("Avg Max Delay", avg_d3qn_delay, avg_ppo_delay))
    
    # Average total loss
    avg_d3qn_loss = np.mean([r['total_loss'] for r in d3qn_results])
    avg_ppo_loss = np.mean([r['total_loss'] for r in ppo_results])
    print("{:<30} {:<15.4f} {:<15.4f}".format("Avg Total Loss", avg_d3qn_loss, avg_ppo_loss))
    
    # Average min bandwidth
    avg_d3qn_bw = np.mean([r['min_bw'] for r in d3qn_results])
    avg_ppo_bw = np.mean([r['min_bw'] for r in ppo_results])
    print("{:<30} {:<15.4f} {:<15.4f}".format("Avg Min Bandwidth", avg_d3qn_bw, avg_ppo_bw))
    
    # Average repeated edges
    avg_d3qn_repeated = np.mean([r['repeated_edges'] for r in d3qn_results])
    avg_ppo_repeated = np.mean([r['repeated_edges'] for r in ppo_results])
    print("{:<30} {:<15.4f} {:<15.4f}".format("Avg Repeated Edges", avg_d3qn_repeated, avg_ppo_repeated))
    
    # Plot comparison charts
    plot_comparison(d3qn_results, ppo_results)
    
    # Save detailed results
    save_detailed_results(d3qn_results, ppo_results, "comparison_results.csv")
    
    return d3qn_results, ppo_results


def plot_comparison(d3qn_results, ppo_results):
    """Plot comparison charts"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    metrics = ['max_delay', 'total_loss', 'min_bw', 'repeated_edges']
    titles = ['Max Delay', 'Total Loss', 'Min Bandwidth', 'Repeated Edges']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx // 2, idx % 2]
        
        d3qn_values = [r[metric] for r in d3qn_results]
        ppo_values = [r[metric] for r in ppo_results]
        
        x = np.arange(len(d3qn_results))
        width = 0.35
        
        ax.bar(x - width/2, d3qn_values, width, label='D3QN', alpha=0.8)
        ax.bar(x + width/2, ppo_values, width, label='PPO', alpha=0.8)
        
        ax.set_xlabel('Topology Index')
        ax.set_ylabel(title)
        ax.set_title(f'Comparison: {title}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison.png', dpi=300)
    print("\nComparison plot saved as 'algorithm_comparison.png'")
    plt.close()


def save_detailed_results(d3qn_results, ppo_results, filename):
    """Save detailed comparison results to CSV"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Topology', 'Algorithm', 'Max Delay', 'Total Loss', 
                        'Min Bandwidth', 'Repeated Edges'])
        
        for i, (d3qn, ppo) in enumerate(zip(d3qn_results, ppo_results)):
            writer.writerow([d3qn['file'], 'D3QN', d3qn['max_delay'], 
                           d3qn['total_loss'], d3qn['min_bw'], d3qn['repeated_edges']])
            writer.writerow([ppo['file'], 'PPO', ppo['max_delay'], 
                           ppo['total_loss'], ppo['min_bw'], ppo['repeated_edges']])
    
    print(f"\nDetailed results saved to '{filename}'")


if __name__ == '__main__':
    # Configuration
    folder_path = 'E:\学术12.16\code\Experimental Dataset/node14_data'
    num_destinations = 3
    src_sw = 2
    dst_sw1 = 6
    num_files = 10  # Test on first 10 topologies
    
    # Run comparison
    d3qn_results, ppo_results = compare_algorithms(
        folder_path, num_destinations, src_sw, dst_sw1, num_files)
    
    print("\nComparison completed!")
