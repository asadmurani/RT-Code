import matplotlib.pyplot as plt
import numpy as np

def plot_comparison(results_part, results_global, results_hybrid):
    labels = ['Partitioned', 'Global', 'Hybrid']
    
    # Extract Metrics
    failed = [results_part['failed_assignments'], results_global['failed_assignments'], results_hybrid['failed_assignments']]
    migrations = [results_part['migrations'], results_global['migrations'], results_hybrid['migrations']]
    missed = [results_part['missed_deadlines'], results_global['missed_deadlines'], results_hybrid['missed_deadlines']]

    x = np.arange(len(labels))  # label locations
    width = 0.25  # width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # We use log scale for Y-axis because Migrations (1000s) are much larger than Failed Assignments (1-5)
    ax.set_yscale('symlog') 

    rects1 = ax.bar(x - width, failed, width, label='Failed Assignments (Fragmentation)', color='red')
    rects2 = ax.bar(x, migrations, width, label='Migrations (Jitter)', color='blue')
    rects3 = ax.bar(x + width, missed, width, label='Missed Deadlines (Performance)', color='orange')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count (Log Scale)')
    ax.set_title('Comparative Analysis: Partitioned vs Global vs Hybrid')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)

    fig.tight_layout()
    plt.savefig('comparative_analysis.png') # Saves the image for your LaTeX report
    plt.show()

def plot_timeline(duration, global_history, hybrid_history):
    """
    Generates a Line Graph showing how Migrations accumulate over time.
    """
    time_axis = np.arange(duration)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Global (Blue)
    ax.plot(time_axis, global_history, label='Global EDF', color='#1f77b4', linewidth=2)
    
    # Plot Hybrid (Green - The proposed solution)
    ax.plot(time_axis, hybrid_history, label='Hybrid EDF', color='green', linewidth=2, linestyle='--')
    
    # Plot Partitioned (Red - Flat line at 0)
    ax.plot(time_axis, [0]*duration, label='Partitioned EDF', color='#d62728', linewidth=2)

    ax.set_ylabel('Cumulative Migrations')
    ax.set_xlabel('Time (Ticks)')
    ax.set_title('System Stability: Migration Overhead Over Time')
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    fig.tight_layout()
    plt.savefig('migration_timeline.png')
    print("Graph saved as 'migration_timeline.png'")
    plt.show()

# --- NEW FUNCTION ADDED BELOW ---

def plot_utilization_heatmap(part_cores, global_cores, hybrid_cores, total_time):
    """
    Generates a heatmap showing the load percentage of every core for every strategy.
    Matches the style of the user provided reference.
    """
    strategies = ["Partitioned", "Global", "Hybrid"]
    num_cores = len(part_cores)
    core_labels = [f"Core {i}" for i in range(num_cores)]

    # 1. Prepare Data
    # Calculate utilization %: (active_time / total_time) * 100
    data = []
    
    # Partitioned Row
    row_part = [(c.active_time / total_time) * 100 for c in part_cores]
    data.append(row_part)
    
    # Global Row
    row_glob = [(c.active_time / total_time) * 100 for c in global_cores]
    data.append(row_glob)
    
    # Hybrid Row
    row_hybr = [(c.active_time / total_time) * 100 for c in hybrid_cores]
    data.append(row_hybr)

    # 2. Setup Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Create Heatmap
    # cmap="YlOrRd" creates the Yellow-Orange-Red gradient
    im = ax.imshow(data, cmap="YlOrRd", vmin=0, vmax=100)

    # 3. Add Labels
    ax.set_xticks(np.arange(len(core_labels)))
    ax.set_yticks(np.arange(len(strategies)))
    ax.set_xticklabels(core_labels)
    ax.set_yticklabels(strategies)

    # Move ticks to bottom and ensure labels are readable
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")

    # 4. Add Colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Core Utilization (%)", rotation=-90, va="bottom")

    # 5. Add Text Annotations (The percentages inside the boxes)
    for i in range(len(strategies)):
        for j in range(len(core_labels)):
            val = data[i][j]
            # Choose text color based on background intensity (White for dark red, Black otherwise)
            text_color = "white" if val > 80 else "black"
            text = ax.text(j, i, f"{val:.1f}%",
                           ha="center", va="center", color=text_color, fontweight='normal')

    ax.set_title("Core Load Balancing & Fragmentation")
    fig.tight_layout()
    
    # Save and Show
    plt.savefig('utilization_heatmap.png')
    print("Graph saved as 'utilization_heatmap.png'")
    plt.show()