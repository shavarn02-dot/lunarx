import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
import seaborn as sns

def generate_benchmark_graph():
    # Setup aesthetic
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Data extracted from benchmark_results.json
    methods = ['ORB', 'SuperPoint', 'SIFT', 'LoFTR']
    inliers = [950, 770, 1329, 4683]
    colors = ['#ff5252', '#ffb142', '#34ace0', '#33d9b2']
    
    bars = ax.bar(methods, inliers, color=colors, width=0.6)
    
    # Customizing axes
    ax.set_ylabel('Number of Verified Inliers', fontsize=14, fontweight='bold', color='white')
    ax.set_title('Matching Performance on Chandrayaan-2 Craters (SIH26166)', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#555555')
    ax.spines['bottom'].set_color('#555555')
    ax.tick_params(axis='x', colors='white', labelsize=13)
    ax.tick_params(axis='y', colors='white', labelsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold', color='white')
                    
    plt.tight_layout()
    out_path = Path('data/outputs/benchmark_graph.png')
    out_path.parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f"Generated {out_path}")

def generate_rmse_graph():
    # Setup aesthetic
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Data extracted from benchmark_results.json
    methods = ['ORB', 'SuperPoint', 'LoFTR', 'SIFT']
    rmse = [0.899, 0.791, 0.257, 0.125]
    colors = ['#ff5252', '#ffb142', '#33d9b2', '#34ace0']
    
    bars = ax.bar(methods, rmse, color=colors, width=0.6)
    
    # Customizing axes
    ax.set_ylabel('Coarse RMSE (Pixels)', fontsize=14, fontweight='bold', color='white')
    ax.set_title('Sub-Pixel Accuracy on Chandrayaan-2 TMC Imagery', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#555555')
    ax.spines['bottom'].set_color('#555555')
    ax.tick_params(axis='x', colors='white', labelsize=13)
    ax.tick_params(axis='y', colors='white', labelsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.3f} px',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold', color='white')
                    
    plt.tight_layout()
    out_path = Path('data/outputs/rmse_graph.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_benchmark_graph()
    generate_rmse_graph()
