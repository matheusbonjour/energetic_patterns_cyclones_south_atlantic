# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    plot_lps.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/27 17:45:49 by daniloceano       #+#    #+#              #
#    Updated: 2024/02/28 16:45:01 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

from lorenz_phase_space.phase_diagrams import Visualizer

from life_cycle import read_life_cycles, convert_counter_to_df


if __name__ == "__main__":
    base_path = '../database_energy_by_periods'  # Adjust to your directory
    output_directory = '../figures/life_cycle_analysis/'
    csv_output_directory = '../csv_life_cycle_analysis/'  # Directory to save CSV files
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(csv_output_directory, exist_ok=True)  # Ensure CSV output directory exists

    # Read life cycles, convert to DataFrame, and filter
    life_cycle_counts = read_life_cycles(base_path)
    life_cycles_df, filtered_life_cycles_df, total_systems = convert_counter_to_df(life_cycle_counts)