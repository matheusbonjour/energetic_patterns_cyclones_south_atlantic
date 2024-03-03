# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    correlation_heatmap_cluster.py                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/02 23:13:30 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/02 23:13:55 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import seaborn as sns
from tqdm import tqdm

def read_and_average_data(base_path):
    """Read CSV files, calculate the mean across all phases for each system, and aggregate into a single DataFrame."""
    all_means = []

    for filename in tqdm(os.listdir(base_path), desc="Reading and averaging data"):
        if filename.endswith('.csv'):
            filepath = os.path.join(base_path, filename)
            try:
                df = pd.read_csv(filepath)
                # Assuming the first column indicates the phase and the rest are terms
                mean_values = df.drop(columns=df.columns[0]).mean()
                all_means.append(mean_values)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Combine all mean values into a single DataFrame
    df_means = pd.DataFrame(all_means)
    return df_means

def plot_correlation_clustermap(df_means, output_filepath):
    """Plot a clustermap of the correlation matrix of the averaged terms."""
    # Calculate the correlation matrix
    corr = df_means.corr()

    # Optional: If you have a categorical variable to differentiate term groups, create a color palette and mapping

    # Draw the clustermap
    g = sns.clustermap(corr, center=0, cmap="vlag",
                       dendrogram_ratio=(.1, .2),
                       cbar_pos=(.02, .32, .03, .2),
                       linewidths=.75, figsize=(12, 13))
    g.ax_row_dendrogram.remove()

    # Save the plot
    g.savefig(output_filepath)
    print(f"Clustermap saved to {output_filepath}")

def main():
    base_path = '../csv_database_energy_by_periods'
    output_directory = '../figures_statistics_energetics/heatmaps/'
    os.makedirs(output_directory, exist_ok=True)
    output_filepath = os.path.join(output_directory, 'terms_correlation_clustermap.png')

    df_means = read_and_average_data(base_path)
    plot_correlation_clustermap(df_means, output_filepath)

if __name__ == "__main__":
    main()
