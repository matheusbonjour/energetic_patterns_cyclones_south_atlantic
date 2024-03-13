# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bivariate_ploy.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/02 19:14:04 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/02 22:54:20 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

def plot_histplot(df, x, y, phase, output_directory, filename_prefix):
    sns.scatterplot(x=x, y=y, data=df, s=5, color=".15", zorder=100)
    sns.histplot(x=x, y=y, data=df, bins=50, pthresh=.1, cmap="mako", zorder=100)
    sns.kdeplot(x=x, y=y, data=df, levels=5, color="w", linewidths=1, zorder=100)
    lowest = min(df[x].min(), df[y].min())
    highest = max(df[x].max(), df[y].max())
    bins = np.linspace(lowest, highest, 50)
    plt.plot(bins, bins, color="red", linewidth=2, zorder=1)
    plt.axhline(y=0, color="k", linewidth=1, zorder=1)
    plt.axvline(x=0, color="k", linewidth=1, zorder=1)
    plt.title(f'{phase.capitalize()} Phase: Histogram of {x} vs {y}')
    save_plot(output_directory, filename_prefix, phase, "histogram")

def plot_joint_kde(df, x, y, phase, output_directory, filename_prefix):
    g = sns.JointGrid(data=df, x=x, y=y, space=0)
    g.plot_joint(sns.kdeplot, fill=True, thresh=0, levels=100, cmap="rocket")
    g.plot_marginals(sns.histplot, color="#03051A", alpha=1, bins=25)
    plt.suptitle(f'{phase.capitalize()} Phase: {x} vs {y} with Marginals', fontsize=16, y=1.02)
    save_plot(output_directory, filename_prefix, phase, "joint_kde", bbox_inches='tight')

def plot_joint_hex(df, x, y, phase, output_directory, filename_prefix):
    sns.jointplot(data=df, x=x, y=y, kind="hex", color="#4CB391", zorder=100)
    plt.suptitle(f'{phase.capitalize()} Phase: Hex Joint Plot of {x} vs {y}', fontsize=16, y=1.02)
    save_plot(output_directory, filename_prefix, phase, "hex", bbox_inches='tight')

def save_plot(output_directory, filename_prefix, phase, plot_type, **savefig_kwargs):
    plot_filename = f"{phase}_{filename_prefix}_{plot_type}.png".replace('/', '_').replace('∂', 'd').replace(' ', '_')
    plot_path = os.path.join(output_directory, plot_filename)
    plt.savefig(plot_path, **savefig_kwargs)
    plt.close()
    print(f"Saved {plot_type} plot for {phase} phase in {plot_path}")

def main():
    base_path = '../csv_database_energy_by_periods'
    output_directory_histplot = '../figures_statistics_energetics/histplot/'
    output_directory_joint_kde = '../figures_statistics_energetics/joint_kde/'
    output_directory_joint_hex = '../figures_statistics_energetics/joint_hex/'
    os.makedirs(output_directory_histplot, exist_ok=True)
    os.makedirs(output_directory_joint_kde, exist_ok=True)
    os.makedirs(output_directory_joint_hex, exist_ok=True)

    systems_energetics = read_and_prepare_data(base_path)
    pairs = [
        ('Ca', 'Ce'),
        ('Ca', 'Ck'),
        ('Ck', 'BKe'),
        ('Ca', 'BAe'),
        ('∂Ae/∂t', 'Ce'),
        ('∂Ae/∂t', 'BAe'),
        ('∂Ke/∂t', 'BKe'),
        ('∂Ke/∂t', 'Ck')
    ]

    phases = ['incipient', 'intensification', 'mature', 'decay', 'intensification 2', 'mature 2', 'decay 2', 'Total']
    for pair in pairs:
        filename_prefix = f"{pair[0]}_vs_{pair[1]}"
        for phase in phases:
            plt.figure(figsize=(10, 6))
            if phase != "Total":
                df_filtered = pd.concat([df[df['Phase'] == phase] for df in systems_energetics.values()], ignore_index=True)
            else:
                # Compute mean values for "Total" phase across all systems and terms
                total_phase_means = pd.concat([df.mean(numeric_only=True).to_frame().T for df in systems_energetics.values()], ignore_index=True)
                total_phase_means['Phase'] = "Total"
                df_filtered = total_phase_means
            
            plot_histplot(df_filtered, pair[0], pair[1], phase, output_directory_histplot, filename_prefix)
            # plot_joint_kde(df_filtered, pair[0], pair[1], phase, output_directory_joint_kde, filename_prefix)
            plot_joint_hex(df_filtered, pair[0], pair[1], phase, output_directory_joint_hex, filename_prefix)

if __name__ == "__main__":
    main()
