# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    life_cycle_by_region.py                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/01 15:35:50 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/01 16:21:38 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

def read_region_system_ids(region_dir):
    """
    Reads system IDs from region-specific files.
    """
    region_ids = {}
    for filename in os.listdir(region_dir):
        if filename.startswith("track_ids_") and filename.endswith(".txt"):
            region = filename.split("_")[2].split(".")[0].upper()
            with open(os.path.join(region_dir, filename), "r") as file:
                ids = [line.strip() for line in file.readlines()]
                region_ids[region] = ids
    return region_ids

def filter_life_cycles_by_region(base_path, region_ids):
    """
    Filters life cycle configurations by genesis region, excluding 'residual' phase.
    """
    life_cycles_by_region = {region: Counter() for region in region_ids}
    
    for region, ids in region_ids.items():
        for system_id in ids:
            file_path = os.path.join(base_path, f"{system_id}_averages.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                # Exclude 'residual' from life cycle configurations
                life_cycle = tuple([phase for phase in df.iloc[:, 0] if 'residual' not in phase])
                life_cycles_by_region[region][life_cycle] += 1
                
    return life_cycles_by_region

def plot_barplot_by_region(life_cycles_by_region, output_directory, total_system_count, region_system_count_df):
    """
    Generates bar plots for life cycle configurations by genesis region.
    """
    letter_codes = {
        'incipient': 'Ic', 'intensification': 'It', 'mature': 'M', 'decay': 'D',
        'incipient 2': 'Ic2', 'intensification 2': 'It2', 'mature 2': 'M2', 'decay 2': 'D2',
        'residual': 'R'
    }

    for region, life_cycles in life_cycles_by_region.items():
        # Prepare DataFrame and calculate percentage
        region_system_count = region_system_count_df.loc[region, 'Total Systems']

        df = pd.DataFrame.from_records([(x, y) for x, y in life_cycles.items()], columns=['Type of System', 'Total Count'])
        df['Percentage'] = (df['Total Count'] / region_system_count) * 100
        df = df[df['Percentage'] >= 1]  # Filter out configurations with less than 1%
        
        df['Type of System'] = df['Type of System'].apply(lambda x: ', '.join([letter_codes.get(phase, phase) for phase in x]))

        df.sort_values('Total Count', ascending=False, inplace=True)

        plt.figure(figsize=(10, len(df) * 0.5))
        sns.barplot(x='Total Count', y='Type of System', hue='Type of System', data=df, palette='pastel')

        for index, (count, pct) in enumerate(zip(df['Total Count'], df['Percentage'])):
            plt.text(count + count * 0.01, index, f"{int(count)} ({pct:.2f}%)", va='center', color='black', weight='bold')

        region_system_percentage_of_total = (region_system_count / total_system_count) * 100
        title = f"Life Cycle Configurations for {region} - {region_system_count} Systems ({region_system_percentage_of_total:.2f}% of Total)"
        plt.title(title)
        plt.tight_layout()

        plot_path = os.path.join(output_directory, f"{region}_life_cycles.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Plot saved for {region} in {plot_path}")

if __name__ == "__main__":
    base_path = '../csv_database_energy_by_periods'
    region_dir = '../csv_life_cycle_analysis'
    output_directory = '../figures_life_cycle_analysis'
    os.makedirs(output_directory, exist_ok=True)
    
    region_ids = read_region_system_ids(region_dir)
    life_cycles_by_region = filter_life_cycles_by_region(base_path, region_ids)

    region_system_count_df = pd.read_csv(os.path.join(region_dir, 'genesis_region_summary.csv'), index_col=0)

    total_system_count = sum(len(ids) for ids in region_ids.values())  # Calculate the total number of systems across all regions
    plot_barplot_by_region(life_cycles_by_region, output_directory, total_system_count, region_system_count_df)