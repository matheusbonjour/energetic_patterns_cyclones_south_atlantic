# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    boxplots.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/02 17:31:28 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/02 18:32:27 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

COLOR_PHASES = {
    'Total': 'grey',
    'incipient': '#65a1e6',
    'intensification': '#f7b538',
    'mature': '#d62828',
    'decay': '#9aa981',
    'intensification 2': '#ca6702',
    'mature 2': '#9b2226',
    'decay 2': '#386641',
    }

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
                df = df.rename(columns={'Unnamed: 0': 'phase'})
                df.index = range(1, len(df) + 1)
                systems_energetics[system_id] = df
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return systems_energetics

def compute_total_phase(systems_energetics):
    """
    Computes the mean values across all phases for each system to represent the "Total" phase.
    """
    for system_id, df in systems_energetics.items():
        mean_values = df.mean(numeric_only=True)
        mean_values['phase'] = 'Total'
        systems_energetics[system_id] = pd.concat([df, pd.DataFrame([mean_values])], ignore_index=True)
    return systems_energetics

def plot_box_plots_by_phase(systems_energetics, output_directory):
    """
    Generates box plots for each term across different life phases, including the mean across all phases.
    """
    all_data = pd.concat(systems_energetics.values(), ignore_index=True)
    terms = [col for col in all_data.columns if col not in ['Unnamed: 0', 'phase', 'system_id']]
    
    for term in terms:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='phase', y=term, data=all_data, palette=COLOR_PHASES.values(),
                     order=['Total', 'incipient', 'intensification', 'mature', 'decay',
                                                             'intensification 2', 'mature 2', 'decay 2'])
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.8, linewidth=0.5)
        plt.title(f'Statistics of {term} by Phase')
        plt.ylabel(f'{term} Value')
        plt.xlabel('Life Cycle Phase')
        
        plot_filename = f'box_plot_{term}.png' if '(finite diff.)' not in term else f'box_plot_budget{term.split("/")[0].split("∂")[1]}.png'
        plot_path = os.path.join(output_directory, plot_filename)
        plt.savefig(plot_path)
        plt.close()
        print(f"Saved {plot_filename} in {output_directory}")

if __name__ == "__main__":
    base_path = '../csv_database_energy_by_periods'
    output_directory = '../figures_statistics_energetics/box_plots/'
    os.makedirs(output_directory, exist_ok=True)

    systems_energetics = read_life_cycles(base_path)
    systems_energetics = compute_total_phase(systems_energetics)
    plot_box_plots_by_phase(systems_energetics, output_directory)