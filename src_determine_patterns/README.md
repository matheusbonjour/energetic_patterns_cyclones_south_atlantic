# Energetic Pattern Determination for Cyclonic Systems

This directory is dedicated to the analysis of energetic patterns within cyclonic systems in the Southern Atlantic, focusing on the computation of average energetic terms across specified life cycle periods.

## Scripts and Outputs

### `export_results.py`
**Purpose**: Processes directories containing Lorenz energy cycle analysis results, calculating average values for specified periods.
**Output**: CSV files for each cyclone system with the average values for specified periods. These files are saved to the `csv_database_energy_by_periods` directory.

### `life_cycle.py`
**Purpose**: Analyzes and visualizes the frequency of different life cycle configurations based on the Lorenz energy cycle data.
**Output**: 
- Bar plots illustrating the distribution of life cycle configurations, saved in the `figures_life_cycle_analysis` directory.
- CSV summary files of life cycle configuration counts and percentages, stored alongside the plots.

### `plot_lps.py`
**Purpose**: Visualizes the energetic data of cyclonic systems in the Lorenz Phase Space, highlighting the dynamic interactions between different energetic components.
**Output**:
- A composite Lorenz Phase Space diagram with data from all analyzed cyclonic systems, as well as each pattern determined by the K-means algorithm, showcasing the energetics' evolution through their life cycles. The diagrams are saved in the `figures_lps/` directory.
