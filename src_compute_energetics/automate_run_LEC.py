import pandas as pd
import os
import subprocess
import time
from tqdm import tqdm

FILTERED_TRACKS = '../tracks_SAt_filtered/tracks_SAt_filtered.csv'
REGION = 'SE-BR'
LEC_PATH = '../lorenz-cycle/lorenz_cycle.py'

tracks = pd.read_csv(FILTERED_TRACKS)
tracks_region = tracks[tracks['region'] == REGION]
system_ids = tracks_region['track_id'].unique()

# Limit to the first 10 cases for testing
system_ids = system_ids[:3]

# Store execution times
execution_times = []

# Change directory to the program directory
os.chdir(os.path.dirname(LEC_PATH))

# Process each system ID
for id in tqdm(system_ids):
    arguments = [f'{id}.nc', '-t', '-r', '-p', '-g', '-v', '--cdsapi']
    command = ['python', LEC_PATH] + arguments

    start_time = time.time()
    subprocess.run(command)
    end_time = time.time()

    # Record the time taken for this execution
    execution_times.append(end_time - start_time)

# Calculate total and mean execution time
total_time = sum(execution_times)
mean_time = total_time / len(execution_times)

print(f'Total time for {len(system_ids)} cases: {total_time:.2f} seconds')
print(f'Mean time per case: {mean_time:.2f} seconds')
