import pandas as pd
import os
import subprocess
import time
from tqdm import tqdm
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    filename='log.automate_run_LEC.txt', 
                    filemode='w')  # 'w' for overwrite, 'a' for append

FILTERED_TRACKS = '../tracks_SAt_filtered/tracks_SAt_filtered.csv'
REGION = 'SE-BR'
LEC_PATH = os.path.abspath('../../lorenz-cycle/lorenz_cycle.py')  # Get absolute path

tracks = pd.read_csv(FILTERED_TRACKS)
tracks_region = tracks[tracks['region'] == REGION]
system_ids = tracks_region['track_id'].unique()

# Limit to the first 3 cases for testing
system_ids = system_ids[:3]

# Store execution times
execution_times = []

try:
    # Change directory to the program directory
    lec_dir = os.path.dirname(LEC_PATH)
    os.chdir(lec_dir)
    logging.info(f"Changed directory to {lec_dir}")
except Exception as e:
    logging.error(f"Error changing directory: {e}")
    exit(1)

try:
    # Pull the latest changes from Git
    subprocess.run(["git", "pull"])
    logging.info("Successfully pulled latest changes from Git")
except Exception as e:
    logging.error(f"Error pulling latest changes from Git: {e}")
    exit(1)

# Process each system ID
for id in tqdm(system_ids):
    arguments = [f'{id}.nc', '-t', '-r', '-p', '-g', '-v', '--cdsapi']
    command = ['python', LEC_PATH] + arguments

    start_time = time.time()
    try:
        subprocess.run(command)
        logging.info(f"Successfully ran Lorenz Cycle script for ID {id}")
    except Exception as e:
        logging.error(f"Error running Lorenz Cycle script for ID {id}: {e}")
        continue
    end_time = time.time()

    # Record the time taken for this execution
    execution_times.append(end_time - start_time)

# Calculate total and mean execution time
total_time = sum(execution_times)
mean_time = total_time / len(execution_times)

logging.info(f'Total time for {len(system_ids)} cases: {total_time:.2f} seconds')
logging.info(f'Mean time per case: {mean_time:.2f} seconds')
