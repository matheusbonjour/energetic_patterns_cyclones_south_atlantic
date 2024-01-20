import pandas as pd
import os
import subprocess
import time
from tqdm import tqdm
import logging
from concurrent.futures import ProcessPoolExecutor

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

# Function to run Lorenz Cycle script for a given system ID
def run_lorenz_cycle(id):
    try:
        arguments = [f'{id}.nc', '-t', '-r', '-p', '-g', '-v', '--cdsapi']
        command = f"python {LEC_PATH} " + " ".join(arguments)
        subprocess.run(command, shell=True, executable='/bin/bash')
        logging.info(f"Successfully ran Lorenz Cycle script for ID {id}")
    except Exception as e:
        logging.error(f"Error running Lorenz Cycle script for ID {id}: {e}")

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

# Store execution times
execution_times = []

# Process each system ID in parallel
start_time = time.time()
with ProcessPoolExecutor() as executor:
    list(tqdm(executor.map(run_lorenz_cycle, system_ids), total=len(system_ids)))
end_time = time.time()

# Record the total time taken for this execution and convert it to hours
total_time_seconds = end_time - start_time
total_time_hours = total_time_seconds / 3600
mean_time_hours = total_time_hours / len(system_ids)

logging.info(f'Total time for {len(system_ids)} cases: {total_time_hours:.2f} hours')
logging.info(f'Mean time per case: {mean_time_hours:.2f} hours')