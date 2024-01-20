# src_compute_energetics

## Overview
This directory contains scripts for pre-processing track data and computing the energetics of cyclones in the South Atlantic . These scripts analyze the filtered data to determine energetic patterns and characteristics of cyclones.

## Scripts

### `select_tracks.py`
- **Purpose**: Filters the raw track data based on specific geographic criteria and time spent over the continent.
- **Key Features**:
  - Reads track data from CSV files.
  - Merges multiple track datasets.
  - Filters tracks based on genesis within predefined regions.
  - Excludes systems spending significant time over the continent.

## Usage
1. **Preparation**: Place raw track data in the `tracks_SAt` directory.
2. **Run Pre-processing**: Execute `src_pre_process_tracks/select_tracks.py` to filter and prepare the track data. 
   - This generates a filtered dataset in `tracks_SAt_filtered`.
4. **Analysis**: Proceed with the analysis of cyclone energetics using the processed data in `tracks_SAt_filtered`.

## Dependencies
- Python 3.9 or higher.
- Libraries: pandas, numpy, matplotlib, and others as required by the scripts.

## Contributing
To contribute to the energetic analysis part of the project:
- Please follow standard coding practices.
- Document any changes or additions made.
- For major changes, open an issue first to discuss what you would like to change.

## Contact
For any queries or contributions, please contact [danilo.oceano@gmail.com](mailto:danilo.oceano@gmail.com).
