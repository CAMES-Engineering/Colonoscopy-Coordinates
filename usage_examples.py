import plot_scripts as ps
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


def plot_multiple_case_tip_paths(source_path, save_dir):
    """
    Plots the tip paths for multiple cases, each with annotated events, and saves the plots in the specified directory.

    Parameters:
    - source_path (str): The base directory containing the data files.
    - save_dir (str): The directory where the generated plots will be saved.

    Outputs:
    - Multiple PNG files saved in the specified directory, each representing the tip path for a case with annotated events.
    """
    results = {}

    # File path to your text file
    file_path = 'SIMMETA.txt'

    # Read the file and process each line
    with open(file_path, 'r') as file:
        for line in file:
            key = line.strip().split(';')[0].split('//')[-1][-3:]
            value = ps.process_line(line)
            if key and value:
                if key not in results:
                    results[key] = []  # create a new list if key doesn't exist
                results[key].append(value)  # append the new value to the list under the key
    print(results)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    for key_check in results.keys():
        colormaps = [plt.cm.Reds, plt.cm.Greens, plt.cm.Blues, plt.cm.Greys, plt.cm.magma]

        fig, ax = plt.subplots(figsize=(15, 10))
        num_datasets = len(results[key_check])
        colorbar_height = 0.07  # Height of each colorbar
        colorbar_width = 0.08  # Width of each colorbar
        spacing = 0.1  # Space between colorbars

        # Adjust main axis to fit colorbars
        ax_position = ax.get_position()
        ax.set_position([
            ax_position.x0,
            ax_position.y0,
            ax_position.width,
            ax_position.height
        ])

        for index, i in enumerate(results[key_check]):
            path = os.path.join(source_path, i)
            X_list, Y_list, Z_list, T_list = ps.get_all_lists_from_path(path)
            cecum_index, _, _, closest_end_index, closest_start_index = ps.get_landmark_indexes(path, T_list)
            negated_X_value = [-z[0] for z in X_list[closest_start_index:cecum_index]]
            negated_Y_value = [-z[0] for z in Y_list[closest_start_index:cecum_index]]
            negated_z_value = [-z[0] for z in Z_list[closest_start_index:cecum_index]]

            # Calculate colors for each point in the current dataset
            cmap = colormaps[index % len(colormaps)]
            colors = cmap(np.linspace(0, 1, len(negated_z_value)))

            ax.scatter(negated_z_value, negated_Y_value, color=colors, label=f'Set {index+1}')

            # Create a separate axis for each colorbar
            colorbar_ax = fig.add_axes([
                ax_position.x1 + 0.01,
                ax_position.y0 + 0.7 - index * (colorbar_height + spacing),  # Position each colorbar
                colorbar_width,
                colorbar_height
            ])
            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), cax=colorbar_ax, orientation='horizontal')
            cbar.set_label(f'Set {index+1}')

        # Configure plot aesthetics
        ax.set_xlabel('Z')
        ax.set_ylabel('Y')
        ax.set_xlim([-500, 0])  # Adjust these limits if necessary
        ax.set_ylim([-250, 300])
        ax.set_title('Scope Tip Intubation Path')
        plt.savefig(os.path.join(save_dir, key_check + '_tip_path.png'), format='png', dpi=300)
        plt.close()


def zeroed_plot_multiple_case_tip_paths(source_path, save_dir):
    """
    Plots heatmaps for multiple cases with zeroed reference points and saves the plots in the specified directory.

    Parameters:
    - source_path (str): The base directory containing the data files.
    - save_dir (str): The directory where the generated plots will be saved.

    Outputs:
    - Multiple PNG files saved in the specified directory, each representing a heatmap for a case.
    """
    results = {}

    # File path to your text file
    file_path = 'SIMMETA.txt'

    # Read the file and process each line
    with open(file_path, 'r') as file:
        for line in file:
            key = line.strip().split(';')[0].split('//')[-1][-3:]
            value = ps.process_line(line)
            if key and value:
                if key not in results:
                    results[key] = []  # create a new list if key doesn't exist
                results[key].append(value)  # append the new value to the list under the key

    print(results)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    for key_check in results.keys():
        fig, ax = plt.subplots(figsize=(15, 10))

        all_adjusted_Z = []
        all_adjusted_Y = []

        for index, i in enumerate(results[key_check]):
            path = os.path.join(source_path, i)
            X_list, Y_list, Z_list, T_list = ps.get_all_lists_from_path(path)
            cecum_index, _, _, closest_end_index, closest_start_index = ps.get_landmark_indexes(path, T_list)
            negated_X_value = [-z[0] for z in X_list[closest_start_index + 5:cecum_index]]
            negated_Y_value = [-z[0] for z in Y_list[closest_start_index + 5:cecum_index]]
            negated_z_value = [-z[0] for z in Z_list[closest_start_index + 5:cecum_index]]
            adjusted_Z = [-z[0] - negated_z_value[0] for z in Z_list[closest_start_index + 5:cecum_index]]
            adjusted_Y = [-y[0] - negated_Y_value[0] for y in Y_list[closest_start_index + 5:cecum_index]]

            all_adjusted_Z.extend(adjusted_Z)
            all_adjusted_Y.extend(adjusted_Y)

        # Create heatmap using gaussian_kde for smoother density estimate
        xy = np.vstack([all_adjusted_Z, all_adjusted_Y])
        kde = gaussian_kde(xy, bw_method=0.1)

        # Create grid for plotting
        x_min, x_max = min(all_adjusted_Z), max(all_adjusted_Z)
        y_min, y_max = min(all_adjusted_Y), max(all_adjusted_Y)
        x_grid, y_grid = np.mgrid[x_min:x_max:400j, y_min:y_max:400j]
        z_grid = np.reshape(gaussian_kde(xy).evaluate(np.vstack([x_grid.ravel(), y_grid.ravel()])), x_grid.shape)

        # Plot heatmap
        cax = ax.imshow(z_grid.T, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='inferno', aspect='auto')
        fig.colorbar(cax, ax=ax, orientation='vertical')

        # Configure plot aesthetics
        ax.set_xlim([x_min, x_max])  # Adjust these limits if necessary
        ax.set_ylim([y_min, y_max])
        ax.set_title('Gaussian KDE Case Heatmap')
        ax.set_xticks([])
        ax.set_yticks([])

        plt.savefig(os.path.join(save_dir, key_check + '_kde.png'), format='png', dpi=300)
        plt.close()


if __name__ == '__main__':
    data_path = 'Processed_delivery/SimBatch'

    zeroed_plot_multiple_case_tip_paths(data_path, 'Multi_tip_case_HeatMaps')
    plot_multiple_case_tip_paths(data_path, 'Multi_tip_case_plots')
