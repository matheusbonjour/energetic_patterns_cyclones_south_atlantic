# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    automate_run_LEC.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/22 13:52:26 by daniloceano       #+#    #+#              #
#    Updated: 2024/01/22 17:19:23 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd
import numpy as np
import os
import subprocess
import time
from tqdm import tqdm
import logging
from concurrent.futures import ProcessPoolExecutor

# # Logging configuration
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s', 
#                     filename='log.automate_run_LEC.txt', 
#                     filemode='w')  # 'w' for overwrite, 'a' for append

FILTERED_TRACKS = '../tracks_SAt_filtered/tracks_SAt_filtered.csv'
REGION = 'SE-BR'
LEC_PATH = os.path.abspath('../../lorenz-cycle/lorenz_cycle.py')  # Get absolute path

class TqdmLoggingHandler(logging.Handler):
    """
    Custom logging handler using tqdm to write log messages.
    """
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
        except Exception:
            self.handleError(record)

def prepare_track_data(system_id):
    """
    Prepare and save track data for a given system ID in the required format.

    Args:
    system_id (int): The ID of the system for which to prepare the track data.
    """
    try:
        track_data = tracks_region[tracks_region['track_id'] == system_id]
        formatted_data = track_data[['date', 'lat vor', 'lon vor', 'vor42']]
        formatted_data.columns = ['time', 'Lat', 'Lon', 'min_max_zeta_850']
        formatted_data['min_max_zeta_850'] = - np.abs(formatted_data['min_max_zeta_850'])
        formatted_data.to_csv('inputs/track', index=False, sep=';')
    except Exception as e:
        logging.error(f"Error preparing track data for ID {system_id}: {e}")

def run_lorenz_cycle(id):
    """
    Run the Lorenz Cycle script for a given system ID after preparing the track data.

    Args:
    id (int): The system ID for which to run the Lorenz Cycle script.
    """
    prepare_track_data(id)
    try:
        arguments = [f'{id}_ERA5.nc', '-t', '-r', '-g', '-v', '-p', '-z', '--cdsapi']
        command = f"python {LEC_PATH} " + " ".join(arguments)
        subprocess.run(command, shell=True, executable='/bin/bash')
        logging.info(f"Successfully ran Lorenz Cycle script for ID {id}")
    except Exception as e:
        logging.error(f"Error running Lorenz Cycle script for ID {id}: {e}")

# Update logging configuration to use the custom handler
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[TqdmLoggingHandler(), 
                              logging.FileHandler('log.automate_run_LEC.txt', mode='w')])

tracks = pd.read_csv(FILTERED_TRACKS)
tracks_region = tracks[tracks['region'] == REGION]
system_ids = tracks_region['track_id'].unique()

# Limit to the first 10 cases for testing
system_ids = system_ids[:2]

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

# Process each system ID in parallel
start_time = time.time()
logging.info(f"Starting {len(system_ids)} cases at {start_time}")

completed_cases = 0
with ProcessPoolExecutor(max_workers=num_workers) as executor:
    for id in executor.map(run_lorenz_cycle, system_ids):
        completed_cases += 1
        if completed_cases % 5 == 0 or completed_cases == len(system_ids):
            logging.info(f"Completed {completed_cases}/{len(system_ids)} cases")

end_time = time.time()
logging.info(f"Finished {len(system_ids)} cases at {end_time}")

# Calculate and log execution times
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60
total_time_hours = total_time_seconds / 3600
mean_time_minutes = total_time_minutes / len(system_ids)
mean_time_hours = total_time_hours / len(system_ids)

logging.info(f'Total time for {len(system_ids)} cases: {total_time_hours:.2f} hours ({total_time_minutes:.2f} minutes)')
logging.info(f'Mean time per case: {mean_time_hours:.2f} hours ({mean_time_minutes:.2f} minutes)')