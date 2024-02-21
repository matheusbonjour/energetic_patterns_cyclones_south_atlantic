import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def process_system_dir(system_dir, base_path):
    """
    Process a single system directory to calculate average values for specified periods.

    Parameters:
    - system_dir: The directory name of the current system being processed.
    - base_path: The base directory path containing all system directories.

    Returns:
    - A tuple containing the system directory name and a DataFrame with average values for each period,
      or None if the required files are not found or an error occurs.
    """
    # Construct the full path to the system directory
    system_path = os.path.join(base_path, system_dir)
    # Try to find the results CSV file by pattern
    results_file = next((f for f in os.listdir(system_path) if f.endswith('track_results.csv')), None)
    if not results_file:
        # Return None if the file is not found
        return system_dir, None

    # Construct the full paths to the results and periods CSV files
    results_path = os.path.join(system_path, results_file)
    periods_path = os.path.join(system_path, 'periods.csv')

    try:
        # Attempt to read the CSV files into DataFrames
        results_df = pd.read_csv(results_path, index_col=0, parse_dates=True)
        periods_df = pd.read_csv(periods_path)
    except FileNotFoundError:
        # Return None if any of the files are not found
        return system_dir, None

    # Initialize a DataFrame to hold the average values for each period
    averages_df = pd.DataFrame(columns=results_df.columns)
    for _, row in periods_df.iterrows():
        # For each period, calculate the average of each column in the results DataFrame
        period_name = row[0]
        start_time = pd.to_datetime(row[1])
        end_time = pd.to_datetime(row[2])
        period_data = results_df.loc[start_time:end_time].mean()
        averages_df.loc[period_name] = period_data

    return system_dir, averages_df

def main(base_path):
    """
    Main function to process all system directories in parallel and save the average values
    for specified periods to CSV files.

    Parameters:
    - base_path: The base directory path containing all system directories.
    """
    # List all directories that match the expected pattern
    system_dirs = [d for d in os.listdir(base_path) if d.endswith('_ERA5_track')]
    system_averages = {}

    # Use a ProcessPoolExecutor to process directories in parallel
    with ProcessPoolExecutor() as executor:
        # Map each system directory to a future task
        future_to_system_dir = {executor.submit(process_system_dir, system_dir, base_path): system_dir for system_dir in system_dirs}
        # Monitor the progress of tasks with a progress bar
        for future in tqdm(as_completed(future_to_system_dir), total=len(system_dirs)):
            system_dir = future_to_system_dir[future]
            try:
                # Attempt to retrieve the result of each task
                _, averages_df = future.result()
                if averages_df is not None:
                    system_averages[system_dir] = averages_df
            except Exception as e:
                print(f"Error processing {system_dir}: {e}")

    # Save the computed averages to CSV files
    output_base_path = os.path.join("../", 'database_energy_by_periods')
    os.makedirs(output_base_path, exist_ok=True)
    for system_dir, averages_df in system_averages.items():
        system_id = system_dir.split('_')[0]
        output_file_path = os.path.join(output_base_path, f"{system_id}_averages.csv")
        averages_df.to_csv(output_file_path)

if __name__ == "__main__":
    base_path = '/home/daniloceano/Documents/Programs_and_scripts/LEC_Results_energetic-patterns'
    main(base_path)
