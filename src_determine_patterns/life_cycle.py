# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    life_cycle.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/22 08:29:32 by daniloceano       #+#    #+#              #
#    Updated: 2024/02/27 17:38:52 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
Life Cycle Analysis for Cyclone Systems

This script performs an analysis of cyclone life cycle configurations from CSV files. Each CSV file
is assumed to contain sequential period data for a given cyclone system. The script reads these CSV files,
counts the occurrences of each unique life cycle configuration, and plots the distributions of these
configurations. It also filters out configurations that represent less than 1% of the total count for
a focused analysis on more prevalent life cycles.

Additionally, the script exports two CSV files containing detailed counts and percentages of life cycle
configurations for both the unfiltered and filtered datasets.

Usage:
- Ensure the 'base_path' variable points to the directory containing your CSV files with life cycle data.
- The 'output_directory' should point to where you want to save the generated plots.
- The 'csv_output_directory' is where the script will save the CSV files with the life cycle counts and percentages.

The script defines the following functions:
- read_life_cycles: Reads CSV files from the specified directory and counts the life cycle configurations.
- convert_counter_to_df: Converts the counts of life cycle configurations into a DataFrame and filters out less common configurations.
- plot_barplot: Generates and saves a bar plot for the life cycle configurations.

After setting the directory paths, the script will automatically read the CSV files, perform the analysis,
generate plots, and export the CSV summaries when executed.

Requirements:
- pandas: For data manipulation and analysis.
- matplotlib and seaborn: For generating plots.
- collections.Counter: For counting life cycle configurations efficiently.

Outputs:
- Bar plots for life cycle configurations (unfiltered and filtered).
- CSV files containing the counts and percentages of life cycle configurations (unfiltered and filtered).
"""

import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns


def read_life_cycles(base_path):
    """
    Reads all CSV files in the specified directory and counts the occurrences of each unique life cycle.

    Parameters:
    - base_path: Path to the directory containing the CSV files with period averages.

    Returns:
    - A Counter object with counts of each unique life cycle configuration.
    """
    life_cycles = Counter()
    
    # Iterate over each file in the directory
    for filename in os.listdir(base_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_path, filename)
            try:
                # Read the periods from the CSV file
                df = pd.read_csv(file_path)
                # Assume first column is the life cycle sequence
                life_cycle = tuple(df.iloc[:, 0])
                # Count the life cycle configuration
                life_cycles[life_cycle] += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return life_cycles

def convert_counter_to_df(life_cycles):
    """
    Converts life cycle counts to a DataFrame and filters out configurations under 1%.
    """
    # Convert the counter to a DataFrame
    life_cycles_df = pd.DataFrame(life_cycles.items(), columns=['Type of System', 'Total Count'])
    total_systems = life_cycles_df['Total Count'].sum()
    life_cycles_df['Percentage'] = (life_cycles_df['Total Count'] / total_systems) * 100
    
    # Filter out configurations under 1%
    filtered_df = life_cycles_df[life_cycles_df['Percentage'] >= 1].copy()
    filtered_df['Type of System'] = filtered_df['Type of System'].apply(lambda x: ', '.join(x))
    filtered_df.sort_values(by='Total Count', ascending=False, inplace=True)
    
    return life_cycles_df, filtered_df, total_systems

def plot_barplot(df, title_suffix, output_directory, filename, total_systems, filtered=False):
    """
    Plots a bar plot for life cycle configurations, including annotations for counts and percentages.
    """
    # Ensure 'Type of System' is a string representation
    df['Type of System'] = df['Type of System'].apply(lambda x: ', '.join(x) if isinstance(x, tuple) else x)

    # Replace full phase names with letter codes
    letter_codes = {'incipient': 'Ic', 'intensification': 'It', 'mature': 'M', 'decay': 'D',
                    'incipient 2': 'Ic2', 'intensification 2': 'It2', 'mature 2': 'M2', 'decay 2': 'D2',
                    'residual': 'R'}
    df['Type of System'] = df['Type of System'].apply(
        lambda x: ', '.join([letter_codes.get(phase.strip(), phase.strip()) for phase in x.split(',')])
    )

    # Sort the DataFrame by 'Total Count'
    df.sort_values('Total Count', inplace=True, ascending=False)

    # Plot configuration
    plt.figure(figsize=(10, len(df) * 0.5))
    bar_plot = sns.barplot(x='Total Count', y='Type of System', data=df, palette='pastel')

    # Annotate each bar with the count and percentage
    for index, (count, pct) in enumerate(zip(df['Total Count'], df['Percentage'])):
        plt.text(count + count * 0.01, index, f"{int(count)} ({pct:.2f}%)", va='center',
                 color='black', weight='bold')

    # Title and labels
    title = f"{title_suffix} (Total Systems: {total_systems})"
    if filtered:
        filtered_count = df['Total Count'].sum()
        filtered_percentage = (filtered_count / total_systems) * 100
        title += f"\nFiltered Count: {filtered_count} - Filtered Percentage: {filtered_percentage:.2f}%"
    plt.title(title)

    # Save the plot
    plt.tight_layout()
    output_path = os.path.join(output_directory, filename)
    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    base_path = '../database_energy_by_periods'  # Adjust to your directory
    output_directory = '../figures/life_cycle_analysis/'
    csv_output_directory = '../csv_life_cycle_analysis/'  # Directory to save CSV files
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(csv_output_directory, exist_ok=True)  # Ensure CSV output directory exists

    # Read life cycles, convert to DataFrame, and filter
    life_cycle_counts = read_life_cycles(base_path)
    life_cycles_df, filtered_life_cycles_df, total_systems = convert_counter_to_df(life_cycle_counts)

    # Export unfiltered life cycle configurations to CSV
    unfiltered_csv_path = os.path.join(csv_output_directory, 'all_life_cycles.csv')
    life_cycles_df.to_csv(unfiltered_csv_path, index=False)
    print(f"Unfiltered life cycle configurations saved to {unfiltered_csv_path}")

    # Export filtered life cycle configurations to CSV
    filtered_csv_path = os.path.join(csv_output_directory, 'filtered_life_cycles.csv')
    filtered_life_cycles_df.to_csv(filtered_csv_path, index=False)
    print(f"Filtered life cycle configurations (>= 1%) saved to {filtered_csv_path}")

    # Call for unfiltered data plot
    plot_barplot(life_cycles_df, 'All Life Cycle Configurations and Counts', output_directory, 'all_life_cycles_plot.png', total_systems)

    # Call for filtered data (>= 1%) plot
    plot_barplot(filtered_life_cycles_df, 'Filtered Configurations (>= 1%)', output_directory, 'filtered_life_cycles_plot.png', total_systems, filtered=True)