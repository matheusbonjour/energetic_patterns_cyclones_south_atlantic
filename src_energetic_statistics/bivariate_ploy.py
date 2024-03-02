# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bivariate_ploy.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/02 19:14:04 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/02 19:14:10 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import matplotlib.pyplot as plt
import seaborn as sns

def plot_bivariate(systems_energetics, pairs, output_directory):
    """
    Plots bivariate plots for specified pairs of terms.
    
    Parameters:
    - systems_energetics: Dictionary with system_id as keys and dataframes as values.
    - pairs: List of tuples, each containing the pair of terms to plot against each other.
    - output_directory: Directory to save the generated plots.
    """
    for pair in pairs:
        plt.figure(figsize=(10, 6))
        for system_id, df in systems_energetics.items():
            # Filter out rows with NaN values in either column of the current pair
            df_filtered = df.dropna(subset=[pair[0], pair[1]])
            # Plot each phase with different colors and markers
            sns.scatterplot(x=pair[0], y=pair[1], data=df_filtered, hue="phase",
                            style="phase", palette="tab10", markers=True, alpha=0.7)
        
        plt.title(f'Bivariate Plot of {pair[0]} vs {pair[1]}')
        plt.xlabel(pair[0])
        plt.ylabel(pair[1])
        plt.legend(title='Life Cycle Phase', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        
        plot_filename = f"bivariate_{pair[0]}_vs_{pair[1]}.png".replace('/', '_').replace('∂', 'd').replace(' ', '_')
        plot_path = os.path.join(output_directory, plot_filename)
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        print(f"Saved plot in {plot_path}")

# Define the pairs of terms for bivariate plots
pairs = [
    ('Ca', 'Ce'),
    ('Ca', 'Ck'),
    ('Ck', 'BKe'),
    ('Ca', 'BAe'),
    ('∂Ae/∂t', 'Ce'),
    ('∂Ae/∂t', 'BAe'),
    ('∂Ke/∂t', 'BKe'),
    ('∂Ke/∂t', 'Ck')
]

# Example call to the function
# Assuming systems_energetics is already defined and contains your data
output_directory = '../figures_statistics_energetics/bivariate_plots/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
plot_bivariate(systems_energetics, pairs, output_directory)
