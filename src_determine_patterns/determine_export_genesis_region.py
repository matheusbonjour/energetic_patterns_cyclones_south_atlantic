# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    determine_export_genesis_region.py                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/01 15:05:41 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/01 15:09:37 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
Export csv files containing track ids of systems with genesis on each region.
"""

import os
import pandas as pd

output_path = "../csv_life_cycle_analysis/"
tracks_database_path = "../tracks_SAt_filtered/"
tracks = pd.read_csv(f"{tracks_database_path}/tracks_SAt_filtered.csv")

genesis_regions = tracks['region'].unique()

for region in genesis_regions:

    filtered_tracks = tracks[tracks['region'] == region]
    systems = list(filtered_tracks['track_id'].unique())

    filename = f"track_ids_{region}.txt"
    with open(f"{os.path.join(output_path, filename)}", "w") as f:
        for system in systems:
            f.write(f"{system}\n")
