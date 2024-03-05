# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    time_series_periods.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/05 19:40:34 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/05 20:02:37 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

COLORS = ['#3B95BF', '#87BF4B', '#BFAB37', '#BF3D3B', '#873e23', '#A13BF0']

def read_and_process_data(base_path):
    all_data = []
    for filename in tqdm(os.listdir(base_path), desc="Reading CSV files"):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_path, filename)
            try:
                df = pd.read_csv(file_path)
                df.rename(columns={'Unnamed: 0': 'phase'}, inplace=True)
                all_data.append(df)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return pd.concat(all_data, ignore_index=True)

def calculate_phase_stats(df):
    phase_stats = df.groupby('phase').agg(['mean', 'std']).reset_index()
    return phase_stats

def plot_time_series_for_group(phase_stats, terms_group, group_name, output_directory):
    plt.figure(figsize=(12, 8))
    phases_ordered = ['incipient', 'intensification', 'mature', 'decay', 'intensification 2', 'mature 2', 'decay 2']
    phase_stats = phase_stats[phase_stats['phase'].isin(phases_ordered)]
    for i, term in enumerate(terms_group):
        if term in phase_stats.columns.levels[0]:
            means = phase_stats[(term, 'mean')].values
            stds = phase_stats[(term, 'std')].values
            plt.plot(phases_ordered, means, label=term, color=COLORS[i])
            plt.fill_between(phases_ordered, means-stds, means+stds, alpha=0.2, color=COLORS[i])
    plt.grid(color='gray', linestyle='--', linewidth=0.5, zorder=1)   
    plt.xlabel('Phase')
    plt.ylabel('Value')
    plt.title(f'{group_name} Averages with Standard Deviation')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    output_path = os.path.join(output_directory, f"{group_name.replace(" ", "_").replace("/", "_")}_time_series.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot to {output_path}")

def main():
    base_path = '../csv_database_energy_by_periods'
    output_directory = '../figures_statistics_energetics/time_series/'
    os.makedirs(output_directory, exist_ok=True)

    df = read_and_process_data(base_path)
    phase_stats = calculate_phase_stats(df)

    # Define groups of terms
    groups = {
        'Energy': ['Az', 'Ae', 'Kz', 'Ke'],
        'Conversion': [col for col in df.columns if col.startswith('C')],
        'Boundary': [col for col in df.columns if col.startswith('B')],
        'Generation/Dissipation': [col for col in df.columns if col.startswith('R') or col.startswith('G')],
        'Budget': [col for col in df.columns if col.startswith('∂')]
    }

    for group_name, terms_group in groups.items():
        plot_time_series_for_group(phase_stats, terms_group, group_name, output_directory)

if __name__ == "__main__":
    main()
