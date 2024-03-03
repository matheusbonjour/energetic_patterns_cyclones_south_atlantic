# Energetic Pattern Analysis for Cyclonic Systems

This directory contains scripts for analyzing and visualizing energetic patterns within cyclonic systems in the Southern Atlantic. These scripts are designed to process, analyze, and visualize data from CSV files containing energetic terms calculated for each system across different life cycle phases.

## Scripts Overview

### `bivariate_plot.py`
**Description**: Generates bivariate plots for selected pairs of energetic terms across different life cycle phases, including an aggregated "Total" phase representing the mean across all phases.
**Output**: Bivariate plots saved in the `../figures_statistics_energetics/bivariate_plots/` directory.

### `boxplots.py`
**Description**: Creates box plots to display statistical distributions of each term across different life cycle phases, including a "Total" phase for aggregated statistics.
**Output**: Box plots saved in the `../figures_statistics_energetics/box_plots/` directory.

### `correlation_heatmap_cluster.py`
**Description**: Constructs a cluster map to visualize the correlation matrix of all terms, averaged across all phases, with hierarchical clustering applied to group similar terms.
**Output**: Cluster maps saved in the `../figures_statistics_energetics/` directory.

### `heatmaps.py`
**Description**: Produces annotated heatmaps for each group of terms (Energy, Conversion, Boundary, Residual, and Budget), displaying the average values across all phases.
**Output**: Heatmaps saved in the `../figures_statistics_energetics/heatmaps/` directory.

### `pdfs.py`
**Description**: Creates ridge plots (also known as Joy plots) and overlapping density plots to visualize the distribution of each term across different life cycle phases.
**Output**: Ridge and density plots saved in the `../figures_statistics_energetics/pdfs/` directory.

## Usage Instructions

1. Ensure that your CSV files containing the energetic terms for each cyclonic system are placed in the `../csv_database_energy_by_periods/` directory.
2. Run each script individually to generate the visualizations. Each script will automatically read the CSV files, perform the necessary data processing, and save the visualizations to the designated output directories.
3. The output directories are specified within each script. You may modify these paths as needed to suit your directory structure.

## Requirements

- Python 3.x
- Pandas
- Matplotlib
- Seaborn
- Numpy
- Scipy (for some scripts)
- tqdm (for progress bars)

Ensure all required libraries are installed in your Python environment before running the scripts.

## Notes

- These scripts are designed for exploratory data analysis and visualization. They provide insights into the energetic dynamics of cyclonic systems across their life cycles.
- The scripts can be modified or extended to accommodate different datasets or additional analyses as needed.

