import os
import pandas as pd

# Assuming 'base_path' is the path to the directory containing all system directories
base_path = "/Users/danilocoutodesouza/Documents/Programs_and_scripts/LEC_Results_energetic-patterns/"
system_dirs = [d for d in os.listdir(base_path) if d.endswith('_ERA5_track')]

# Initialize a dictionary to hold the results DataFrame for each system
system_averages = {}

for system_dir in system_dirs:
    system_path = os.path.join(base_path, system_dir)
    # Dynamically identify the results_track.csv file by its pattern
    results_file = next((f for f in os.listdir(system_path) if f.endswith('track_results.csv')), None)
    if not results_file:
        print(f"No results_track.csv file found in {system_dir}")
        continue  # Skip this directory if the file is not found

    results_path = os.path.join(system_path, results_file)
    periods_path = os.path.join(system_path, 'periods.csv')
    
    try:
        # Load the results and periods data
        results_df = pd.read_csv(results_path, index_col=0, parse_dates=True)
        periods_df = pd.read_csv(periods_path)
    except FileNotFoundError as e:
        print(e)
        continue  # Skip this iteration if files are not found

    # Prepare a DataFrame to hold averages for this system
    averages_df = pd.DataFrame(columns=results_df.columns)
    
    for _, row in periods_df.iterrows():
        period_name = row[0]
        start_time = pd.to_datetime(row[1])
        end_time = pd.to_datetime(row[2])
        
        # Filter results_df to the current period and compute averages
        period_data = results_df.loc[start_time:end_time].mean()
        averages_df.loc[period_name] = period_data
    
    # Store the averages DataFrame in the dictionary
    system_averages[system_dir] = averages_df

# At this point, 'system_averages' contains a DataFrame for each system with the requested averages
print(system_averages)