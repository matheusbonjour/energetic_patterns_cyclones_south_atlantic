# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    plot_lps.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/27 17:45:49 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/04 09:54:39 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import os
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from lorenz_phase_space.phase_diagrams import Visualizer

def read_life_cycles(base_path):
    """
    Reads all CSV files in the specified directory and collects DataFrame for each system.
    """
    systems_energetics = {}
    
    for filename in tqdm(os.listdir(base_path), desc="Reading CSV files"):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_path, filename)
            system_id = filename.split('_')[0]
            try:
                df = pd.read_csv(file_path)
                systems_energetics[system_id] = df
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return systems_energetics

def read_patterns(patterns_by_life_cycle_paths):
    """
    Reads all CSV files in the specified directory and collects DataFrame for each system.
    """
    patterns_energetics = {}
    for directory in patterns_by_life_cycle_paths:
        life_cycle_type = os.path.basename(directory)
        patterns = glob(f'{directory}/*')
        for pattern in patterns:
            df = pd.read_csv(pattern)
            cluster = os.path.basename(pattern).split('_')[1]
            patterns_energetics[f"{life_cycle_type}_{cluster}"] = df
    return patterns_energetics

def plot_system(lps, df):
    """
    Plots the Lorenz Phase Space diagram for a single system
    """
    # Generate the phase diagram
    lps.plot_data(
        x_axis=df['Ck'],
        y_axis=df['Ca'],
        marker_color=df['Ge'],
        marker_size=df['Ke']
    )

def determine_global_limits(systems_energetics):
    x_min, x_max = float('inf'), float('-inf')
    y_min, y_max = float('inf'), float('-inf')
    color_min, color_max = float('inf'), float('-inf')
    size_min, size_max = float('inf'), float('-inf')

    for df in systems_energetics.values():
        x_min = min(x_min, df['Ck'].min())
        x_max = max(x_max, df['Ck'].max())
        y_min = min(y_min, df['Ca'].min())
        y_max = max(y_max, df['Ca'].max())
        color_min = min(color_min, df['Ge'].min())
        color_max = max(color_max, df['Ge'].max())
        size_min = min(size_min, df['Ke'].min())
        size_max = max(size_max, df['Ke'].max())

    return [x_min - 5, x_max + 5], [y_min - 5, y_max + 5], [color_min, color_max], [size_min, size_max]

def plot_all_systems(base_path, output_directory):
    # Read the energetics data for all systems
    systems_energetics = read_life_cycles(base_path)

    # Initialize the Lorenz Phase Space plotter
    lps = Visualizer(LPS_type='mixed', zoom=False)

    # Plot each system onto the Lorenz Phase Space diagram
    for system_id, df in tqdm(systems_energetics.items(), desc="Plotting systems"):
        plot_system(lps, df)
    
    # Save the final plot
    plot_filename = 'lps_all_systems.png'
    plot_path = os.path.join(output_directory, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Final plot saved to {plot_path}")

    # Determine global limits
    x_limits, y_limits, color_limits, marker_limits = determine_global_limits(systems_energetics)

    # Initialize Lorenz Phase Space with dynamic limits and zoom enabled
    lps = Visualizer(
        LPS_type='mixed',
        zoom=True,
        x_limits=x_limits,
        y_limits=y_limits,
        color_limits=color_limits,
        marker_limits=marker_limits
    )

    # Plot each system onto the Lorenz Phase Space diagram
    for system_id, df in tqdm(systems_energetics.items(), desc="Plotting systems"):
        lps.plot_data(
            x_axis=df['Ck'],
            y_axis=df['Ca'],
            marker_color=df['Ge'],
            marker_size=df['Ke']
        )

    # Save the final plot
    plot_filename = 'lps_all_systems_zoom.png'
    plot_path = os.path.join(output_directory, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Final plot saved to {plot_path}")

def plot_all_patterns(base_path, output_directory):
    # Read the energetics data for patterns
    patterns_path = "../csv_patterns/"
    patterns_by_life_cycle_paths = glob(f'{patterns_path}/*')

    patterns_energetics = read_patterns(patterns_by_life_cycle_paths)

    # Initialize the Lorenz Phase Space plotter
    lps = Visualizer(LPS_type='mixed', zoom=False)

    # Plot each system onto the Lorenz Phase Space diagram
    for system_id, df in tqdm(patterns_energetics.items(), desc="Plotting systems"):
        plot_system(lps, df)

    # Save the final plot
    plot_filename = 'lps_all_patterns.png'
    plot_path = os.path.join(output_directory, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Final plot saved to {plot_path}")

    # Determine global limits
    x_limits, y_limits, color_limits, marker_limits = determine_global_limits(patterns_energetics)

    # Initialize Lorenz Phase Space with dynamic limits and zoom enabled
    lps = Visualizer(
        LPS_type='mixed',
        zoom=True,
        x_limits=x_limits,
        y_limits=y_limits,
        color_limits=color_limits,
        marker_limits=marker_limits
    )

    # Plot each system onto the Lorenz Phase Space diagram
    for species, df in tqdm(patterns_energetics.items(), desc="Plotting systems"):
        print(f"Plotting {species}")
        lps.plot_data(
            x_axis=df['Ck'],
            y_axis=df['Ca'],
            marker_color=df['Ge'],
            marker_size=df['Ke']
        )

    # Save the final plot
    plot_filename = 'lps_all_patterns_zoom.png'
    plot_path = os.path.join(output_directory, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Final plot saved to {plot_path}")

def plot_clusters(base_path, output_directory):
    # Read the energetics data for patterns
    patterns_path = "../csv_patterns/"
    patterns_by_life_cycle_paths = glob(f'{patterns_path}/*')

    for directory in patterns_by_life_cycle_paths:
        life_cycle_type = os.path.basename(directory)
        patterns = glob(f'{directory}/*')

        patterns_energetics = {}

        for pattern in patterns:
            df = pd.read_csv(pattern)
            cluster = os.path.basename(pattern).split('_')[1]
            patterns_energetics[cluster] = df

        # Determine global limits
        x_limits, y_limits, color_limits, marker_limits = determine_global_limits(patterns_energetics)

        # Initialize the Lorenz Phase Space plotter with dynamic limits and zoom enabled
        lps = Visualizer(
            LPS_type='mixed',
            zoom=True,
            x_limits=x_limits,
            y_limits=y_limits,
            color_limits=color_limits,
            marker_limits=marker_limits
        )

        # Plot each system onto the Lorenz Phase Space diagram
        for cluster, df in patterns_energetics.items():
            plot_system(lps, df)

        title = life_cycle_type.replace(
            "Ic", "Incipient").replace(
            "It", "Intensification").replace(
            "M", "Mature").replace(
            "D", "Decay").replace(
            "It2", "Intensification 2").replace(
            "M2", "Mature 2").replace(
            "D2", "Decay 2")
        plt.title(f"Life cycle type: {title}")

        # Save the final plot
        plot_filename = f'lps_{life_cycle_type}.png'
        plot_path = os.path.join(output_directory, plot_filename)
        plt.savefig(plot_path)
        plt.close()
        print(f"Final plot saved to {plot_path}")

if __name__ == "__main__":
    base_path = '../csv_database_energy_by_periods'
    output_directory = '../figures_lps/'
    os.makedirs(output_directory, exist_ok=True)

    # First: plot all systems
    plot_all_systems(base_path, output_directory)

    # Now, plot just the patterns 
    plot_all_patterns(base_path, output_directory)

    # Finally, plot clusters for each pattern in distinct plots
    plot_clusters(base_path, output_directory)