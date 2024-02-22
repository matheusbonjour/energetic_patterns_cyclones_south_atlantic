# South Atlantic Cyclone Energetics Patterns Project

## Overview
This repository contains the work related to identifying and analyzing the energetic patterns of cyclones in the South Atlantic. It encompasses the processes from pre-processing cyclone track data to detailed energetics computations. The project's structure facilitates a methodical approach to each stage of the analysis.

## Directory Structure
- `natural_earth_continents`: Hosts geographical shapefiles necessary for cyclone track data filtering.
- `src_pre_process_tracks`: Includes scripts responsible for the initial pre-processing of cyclone track data.
- `tracks_SAt`: Contains the original cyclone track data set for the South Atlantic.
- `tracks_SAt_filtered`: Stores cyclone track data that has been processed and is ready for further analysis.
- `src_compute_energetics`: Scripts for computing the energetics of cyclone systems from the processed track data.
- `src_determine_patterns`: Contains scripts for determining the life cycle and energetic patterns from the computed energetics.
- `figures`: Visualization outputs such as plots and graphs are saved here.
- `database_energy_by_periods`: The computed averages for different energetic terms across specified periods are stored here as CSV files.

## Dependencies
To run the scripts in this repository, the following dependencies are required:
- Python 3.9 or higher
- Essential Python libraries including pandas, numpy, geopandas, tqdm, matplotlib, and seaborn

The `natural_earth_continents` directory must have the necessary shapefiles for continent filtering to work correctly.