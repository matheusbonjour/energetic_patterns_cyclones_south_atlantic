# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    eof_analysis.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/03 16:49:11 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/05 09:15:49 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from eofs.standard import Eof
from pyEOF import *

def read_and_prepare_data(base_path):
    all_dfs = []

    for filename in tqdm(os.listdir(base_path), desc="Reading CSV files"):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_path, filename)
            try:
                df = pd.read_csv(file_path)
                df = df.rename(columns={'Unnamed: 0': 'Phase'})
                df.columns = [col if '∂' not in col else '∂' + col.split('∂')[1].split('/')[0] + '/∂t' for col in df.columns]

                # Add 'system_id' column
                system_id = filename.split('_')[0]
                df['system_id'] = system_id

                # Add a 'Total' phase with the average across phases
                total_row = df.drop(columns=['Phase', 'system_id']).mean(axis=0)
                total_row['Phase'] = 'Total'
                total_row['system_id'] = system_id
                df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
                
                all_dfs.append(df)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_dfs, ignore_index=True)
    return combined_df

def compute_eofs(df, output_directory):
    """Compute EOFs for each term across all periods and for each period individually."""
    phases = ['incipient', 'intensification', 'mature', 'decay', 'intensification 2', 'mature 2', 'decay 2', 'Total']

    for phase in phases:
        # Get data for the current phase
        phase_df = df[df['Phase'] == phase].drop(columns=['Phase', 'system_id'])

        # Step 1: Compute sample mean
        sample_mean = phase_df.mean(axis=0)
        
        # Step 2: Subtract sample mean to obtain anomalies
        anomalies = phase_df - sample_mean
        
        # Step 3: Compute standard deviation
        std_deviation = phase_df.std(axis=0)
        
        # Step 4: Normalize by dividing by standard deviation
        normalized_anomalies = anomalies / std_deviation

        # Compute EOFs
        # solver = Eof(normalized_anomalies.values)

        # # Compute EOFs for each term
        # eofs = solver.eofsAsCovariance(neofs=3)
        # pcs = solver.pcs(npcs=3, pcscaling=1)
        # variance_fraction = solver.varianceFraction(neigs=3)

        # Compute EOFs with PyEOF
        n = 4
        pca = df_eof(normalized_anomalies, n_components=n)
        eofs = pca.eofs(s=2, n=n) # get eofs
        pcs = pca.pcs(s=2, n=n) # get pcs
        variance_fraction = pca.evf(n=n) # get variance fraction



        # Save EOFs, PCs, and variance fraction to files
        phase_output_directory = os.path.join(output_directory, phase)
        os.makedirs(phase_output_directory, exist_ok=True)
        np.savetxt(os.path.join(phase_output_directory, 'eofs.csv'), eofs, delimiter=',')
        np.savetxt(os.path.join(phase_output_directory, 'pcs.csv'), pcs, delimiter=',')
        np.savetxt(os.path.join(phase_output_directory, 'variance_fraction.csv'), variance_fraction, delimiter=',')

        print(f"EOF analysis for phase {phase} complete and saved to files.")

def main():
    base_path = '../csv_database_energy_by_periods'
    output_directory = '../csv_eofs_energetics/'
    os.makedirs(output_directory, exist_ok=True)

    df = read_and_prepare_data(base_path)
    compute_eofs(df, output_directory)

if __name__ == "__main__":
    main()
