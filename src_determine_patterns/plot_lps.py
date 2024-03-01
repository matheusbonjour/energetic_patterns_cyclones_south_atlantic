# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    plot_lps.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/27 17:45:49 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/01 11:50:52 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import os
import pandas as pd
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

    return [x_min, x_max], [y_min, y_max], [color_min, color_max], [size_min, size_max]

if __name__ == "__main__":
    base_path = '../database_energy_by_periods'
    output_directory = '../figures_lps/'
    os.makedirs(output_directory, exist_ok=True)

    # Initialize the Lorenz Phase Space plotter
    lps = Visualizer(LPS_type='mixed', zoom=False)

    # Read the energetics data for all systems
    systems_energetics = read_life_cycles(base_path)

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