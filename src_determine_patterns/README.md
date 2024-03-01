# Energetic Pattern Determination for Cyclonic Systems

This directory is dedicated to the analysis of energetic patterns within cyclonic systems in the Southern Atlantic, focusing on the computation of average energetic terms across specified life cycle periods.

## Scripts and Outputs

### `export_results.py`
**Purpose**: Processes directories containing Lorenz energy cycle analysis results, calculating average values for specified periods.  
**Output**: CSV files for each cyclone system with the average values for specified periods. These files are saved to the `csv_database_energy_by_periods` directory.

### `determine_export_genesis_region.py`
**Purpose**: Determine which systems had genesis on each cyclogenesis region on the Southern Atlantic (ARG, LA-PLATA, and SE-BR).  
**Output**: Text files containing track ids of systems that had genesis on each respective region. These files are saved to the `csv_life_cycle_analysis` directory.

### `life_cycle.py`
**Purpose**: Analyzes and visualizes the frequency of different life cycle configurations based on the Lorenz energy cycle data.  
**Output**: 
- Bar plots illustrating the distribution of life cycle configurations, saved in the `figures_life_cycle_analysis` directory.
- CSV summary files of life cycle configuration counts and percentages, stored alongside the plots.

### `plot_lps.py`
**Purpose**: Visualizes the energetic data of cyclonic systems in the Lorenz Phase Space, highlighting the dynamic interactions between different energetic components.  
**Output**:
- A composite Lorenz Phase Space diagram with data from all analyzed cyclonic systems, showcasing the energetics' evolution through their life cycles. The diagrams are saved in the `figures_lps/` directory.

### `life_cycle_by_region.py`
**Purpose**: Analyzes and visualizes the frequency of different life cycle configurations based on the Lorenz energy cycle data for systems originating from specific genesis regions in the Southern Atlantic.  
**Output**: 
- Bar plots illustrating the distribution of life cycle configurations by genesis region, highlighting regional differences in cyclogenesis patterns. These plots are saved in the `figures_life_cycle_analysis` directory.
- CSV files detailing the life cycle configuration counts and percentages for systems from each genesis region, providing insight into regional variations in cyclone development.

