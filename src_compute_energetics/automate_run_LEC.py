# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    automate_run_LEC.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/22 13:52:26 by daniloceano       #+#    #+#              #
#    Updated: 2024/02/02 10:36:48 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import glob
import subprocess
import time
import logging
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor

FILTERED_TRACKS = '../tracks_SAt_filtered/tracks_SAt_filtered.csv'
REGION = 'ARG'
LEC_PATH = os.path.abspath('../../lorenz-cycle/lorenz_cycle.py')  # Get absolute path
LEC_RESULTS_DIR = os.path.abspath('../../LEC_Results')  # Get absolute PATH

CDSAPI_PATH = os.path.expanduser('~/.cdsapi')
SUBPROCESS_BATCH_SIZE = 50  # Number of subprocesses after which to switch .cdsapi file

def count_evaluated_systems():
    """
    Counts the number of systems that have been evaluated based on the presence of results files.

    Returns:
    int: The number of evaluated systems.
    """
    evaluated_count = 0
    for dirname in os.listdir(LEC_RESULTS_DIR):
        if dirname.endswith('_ERA5_track') and os.path.exists(os.path.join(LEC_RESULTS_DIR, dirname, f"{dirname}_results.csv")):
            evaluated_count += 1
    return evaluated_count

def get_cdsapi_keys():
    """
    Lists all files in the home directory that match the pattern 'cdsapi-*'.

    Returns:
    list: A list of filenames matching the pattern.
    """
    home_dir = os.path.expanduser('~')
    pattern = os.path.join(home_dir, 'cdsapi-*')
    files = glob.glob(pattern)
    # Extract file suffixes from the full paths
    suffixes = [os.path.basename(file) for file in files]
    return suffixes

def copy_cdsapi(suffix):
    """
    Copies a specific .cdsapi file to the default .cdsapi location.
    Args:
    suffix (str): The suffix of the .cdsapi file to be copied.
    """
    try:
        source_path = os.path.expanduser(f'~/{suffix}')
        subprocess.run(['cp', source_path, CDSAPI_PATH], check=True)
        logging.info(f"Copied {source_path} to {CDSAPI_PATH}")
    except Exception as e:
        logging.error(f"Error copying {source_path} to {CDSAPI_PATH}: {e}")


def prepare_track_data(system_id):
    """
    Prepare and save track data for a given system ID in the required format.
    Each system ID will have its own input file.

    Args:
    system_id (int): The ID of the system for which to prepare the track data.
    """
    try:
        track_data = tracks_region[tracks_region['track_id'] == system_id]
        # Explicitly create a copy of the DataFrame to avoid SettingWithCopyWarning
        formatted_data = track_data[['date', 'lat vor', 'lon vor', 'vor42']].copy()
        formatted_data.columns = ['time', 'Lat', 'Lon', 'min_max_zeta_850']
        formatted_data['min_max_zeta_850'] = - np.abs(formatted_data['min_max_zeta_850'])
        # Create a unique input file for each system ID
        input_file_path = f'inputs/track_{system_id}.csv'
        formatted_data.to_csv(input_file_path, index=False, sep=';')
        return input_file_path
    except Exception as e:
        logging.error(f"Error preparing track data for ID {system_id}: {e}")
        return None
    
def check_results_exist(system_id):
    """
    Check if results for the given system ID already exist.

    Args:
    system_id (int): The system ID to check.

    Returns:
    bool: True if results exist, False otherwise.
    """
    results_file_path = os.path.join(LEC_RESULTS_DIR, f"{system_id}_ERA5_track", f"{system_id}_ERA5_track_results.csv")
    return os.path.exists(results_file_path)

def run_lorenz_cycle(id):
    global subprocess_counter
    subprocess_counter += 1

    if check_results_exist(id):
        logging.info(f"Results already exist for system ID {id}, skipping.")
        return id

    # Switch .cdsapi file for every SUBPROCESS_BATCH_SIZE subprocesses
    if subprocess_counter % SUBPROCESS_BATCH_SIZE == 0:
        suffix_index = (subprocess_counter // SUBPROCESS_BATCH_SIZE - 1) % len(CDSAPI_SUFFIXES)
        copy_cdsapi(CDSAPI_SUFFIXES[suffix_index])
        logging.info(f"Switched .cdsapi file to {CDSAPI_SUFFIXES[suffix_index]}")

    input_track_path = prepare_track_data(id)
    if input_track_path:
        try:
            arguments = [f'{id}_ERA5.nc', '-t', '-r', '-g', '-v', '-p', '-z', '--cdsapi', '--trackfile', input_track_path]
            command = f"python {LEC_PATH} " + " ".join(arguments)
            subprocess.run(command, shell=True, executable='/bin/bash')
            logging.info(f"Successfully ran Lorenz Cycle script for ID {id}")
        except Exception as e:
            logging.error(f"Error running Lorenz Cycle script for ID {id}: {e}")
    else:
        logging.error(f"Error running Lorenz Cycle script for ID {id}: Could not prepare track data")

    return id


CDSAPI_SUFFIXES = get_cdsapi_keys()

# Initialize subprocess_counter with the number of already evaluated systems
subprocess_counter = count_evaluated_systems()

# Update logging configuration to use the custom handler
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.automate_run_LEC.txt', mode='w')])

logging.info(f"Starting automate_run_LEC.py for region: {REGION}")

tracks = pd.read_csv(FILTERED_TRACKS)
tracks_region = tracks[tracks['region'] == REGION]
system_ids = tracks_region['track_id'].unique()

# Change directory to the Lorenz Cycle program directory
try:
    lec_dir = os.path.dirname(LEC_PATH)
    os.chdir(lec_dir)
    logging.info(f"Changed directory to {lec_dir}")
except Exception as e:
    logging.error(f"Error changing directory: {e}")
    exit(1)

# Pull the latest changes from Git
try:
    subprocess.run(["git", "pull"])
    logging.info("Successfully pulled latest changes from Git")
except Exception as e:
    logging.error(f"Error pulling latest changes from Git: {e}")
    exit(1)

# Determine the number of CPU cores to use
max_cores = os.cpu_count()
num_workers = max(1, max_cores - 4) if max_cores else 1
logging.info(f"Using {num_workers} CPU cores")

# Process each system ID in parallel and log progress
start_time = time.time()
formatted_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
logging.info(f"Starting {len(system_ids)} cases at {formatted_start_time}")

completed_cases = 0
with ProcessPoolExecutor(max_workers=num_workers) as executor:
    for completed_id in executor.map(run_lorenz_cycle, system_ids):
        completed_cases += 1
        logging.info(f"Completed {completed_cases}/{len(system_ids)} cases (ID {completed_id})")
        
end_time = time.time()
formatted_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
logging.info(f"Finished {len(system_ids)} cases at {formatted_end_time}")

# Calculate and log execution times
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60
total_time_hours = total_time_seconds / 3600
mean_time_minutes = total_time_minutes / len(system_ids)
mean_time_hours = total_time_hours / len(system_ids)

logging.info(f'Total time for {len(system_ids)} cases: {total_time_hours:.2f} hours ({total_time_minutes:.2f} minutes)')
logging.info(f'Mean time per case: {mean_time_hours:.2f} hours ({mean_time_minutes:.2f} minutes)')