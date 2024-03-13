# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    heatmaps.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/02 18:37:40 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/02 19:16:03 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

def read_and_prepare_data(base_path):
    systems_energetics = {}

    for filename in tqdm(os.listdir(base_path), desc="Reading CSV files"):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_path, filename)
            try:
                df = pd.read_csv(file_path)
                df = df.rename(columns={'Unnamed: 0': 'Phase'})
                df.columns = [col if '∂' not in col else '∂' + col.split('∂')[1].split('/')[0] + '/∂t' for col in df.columns]
                systems_energetics[filename.split('_')[0]] = df
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return systems_energetics

def compute_statistics(systems_energetics):
    all_data = pd.concat(systems_energetics.values(), ignore_index=True)
    statistics_df = all_data.groupby('Phase').mean().T
    return statistics_df

def plot_annotated_heatmap_by_category(statistics_df, category, terms, output_directory):
    phase_order = ['incipient', 'intensification', 'mature', 'decay', 'intensification 2', 'mature 2', 'decay 2']
    
    # Filter DataFrame to include only the specified phases, maintaining the order
    filtered_df = statistics_df[phase_order].loc[terms].dropna(how='all')  # Filter and drop terms that are all NaN
    max_abs_value = np.max(np.abs(filtered_df.values))  # Find the max absolute value for centering the color bar
    
    plt.figure(figsize=(12, len(filtered_df) / 2))
    sns.heatmap(filtered_df, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                vmin=-max_abs_value, vmax=max_abs_value, cbar_kws={'label': 'Mean Value'})
    plt.title(f"{category.replace('_', '/')} Terms")
    plt.ylabel("")
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plot_path = os.path.join(output_directory, f"annotated_heatmap_{category}.png")
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    print(f"Saved {category} terms annotated heatmap in {plot_path}")

if __name__ == "__main__":
    base_path = '../csv_database_energy_by_periods'
    output_directory = '../figures_statistics_energetics/heatmaps/'
    os.makedirs(output_directory, exist_ok=True)

    systems_energetics = read_and_prepare_data(base_path)
    statistics_df = compute_statistics(systems_energetics)

    categories = {
        'Energy': ['A', 'K'],
        'Conversion': ['C'],
        'Boundary': ['B'],
        'Generation_Dissipation': ['G', 'R'],
        'Budgets': ['∂']
    }

    for category, prefixes in categories.items():
        terms = [term for term in statistics_df.index if any(term.startswith(prefix) for prefix in prefixes)]
        plot_annotated_heatmap_by_category(statistics_df, category, terms, output_directory)
