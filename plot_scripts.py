import os
import cv2 
import PIL
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from scipy.signal import savgol_filter


def moving_average(data, window_size):
    """
    Calculate the moving average of a given data set using a specified window size.

    Parameters:
    data (list or array): The input data set.
    window_size (int): The size of the moving window.

    Returns:
    np.array: The moving average of the data set.
    """
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')


def get_fractional_indexes(data, fraction=12):
    """
    Calculate the indexes for fractional parts of the data list.

    Parameters:
    data (list): The input data list.
    fraction (int): The number of equal fractions to divide the data into.

    Returns:
    list: A list of indexes corresponding to each fraction.
    """
    n = len(data)
    frac_list = []
    for i in range(fraction - 1):
        frac_list.append(int(n * (i + 1) / fraction))
    frac_list.append(n - 1)
    return frac_list


def process_line(line):
    """
    Process a line of text by splitting and extracting specific parts.

    Parameters:
    line (str): The input line of text.

    Returns:
    str or None: The extracted value or None if the line is improperly formatted.
    """
    parts = line.strip().split(';')
    if len(parts) < 3:
        return None
    index_2 = parts[2]
    return index_2


def get_list_from_txt(path):
    """
    Read a text file and convert its contents to a list of lists of floats.

    Parameters:
    path (str): The file path to read from.

    Returns:
    list: A list of lists, where each sublist contains floats.
    """
    coord_list = []
    with open(path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        temp_list = [float(i) for i in line.strip().split(';')[:-1]]
        coord_list.append(temp_list)

    return coord_list


def get_all_coord_paths(path):
    """
    Generate file paths for coordinate data files (X, Y, Z, T).

    Parameters:
    path (str): The base directory path.

    Returns:
    tuple: A tuple containing file paths for X, Y, Z, and T data files.
    """
    return (
        os.path.join(path, 'X.txt'),
        os.path.join(path, 'Y.txt'),
        os.path.join(path, 'Z.txt'),
        os.path.join(path, 'T.txt')
    )


def get_all_lists_from_path(path):
    """
    Read coordinate data from specified directory and return as lists.

    Parameters:
    path (str): The base directory path.

    Returns:
    tuple: A tuple containing lists of X, Y, Z coordinates and T times.
    """
    X_path, Y_path, Z_path, T_path = get_all_coord_paths(path)
    X_list = get_list_from_txt(X_path)
    Y_list = get_list_from_txt(Y_path)
    Z_list = get_list_from_txt(Z_path)
    T_list = [item[0] for item in get_list_from_txt(T_path)]

    return X_list, Y_list, Z_list, T_list


def get_landmark_indexes(path, T_list):
    """
    Process a log file and return the indexes of specific landmarks (Cecum, Flexur L, Flexur R, Start, End).

    Parameters:
    path (str): The directory path containing the log file.
    T_list (list): A list of time coordinates.

    Returns:
    tuple: A tuple containing the indexes of the landmarks in the following order:
           (cecum_index, flexur_L_index, flexur_R_index, end_index, start_index)
    """

    def calculate_index(event_time, end_coordinates_time, end_time, T_list):
        """
        Calculate the index of the event closest to the given event_time in T_list.

        Parameters:
        event_time (float): The time of the event.
        end_coordinates_time (float): The last coordinate time in T_list.
        end_time (float): The end time from the log file.
        T_list (list): A list of time coordinates.

        Returns:
        int: The index of the closest time in T_list to the event_time.
        """
        adjusted_time = end_coordinates_time - (end_time - (event_time * 1000))
        closest_value = min(T_list, key=lambda x: abs(x - adjusted_time))
        return T_list.index(closest_value)

    index_path = os.path.join(path, 'LogFile_P.txt')
    landmarks = {
        'Cecum': 0,
        'Fleksur L': 0,
        'Fleksur R': 0,
        'Start': 0,
        'End': 0
    }
    cecum_found = False

    with open(index_path, 'r') as file:
        lines = file.readlines()

    end_coordinates_time = T_list[-1]
    end_time = float(lines[-1].split(';')[0]) * 1000

    for line in lines:
        timestamp, event = line.split(';')[0], line.split(';')[1]

        if 'Endoscopy started' in event:
            start_time = float(timestamp)
            landmarks['Start'] = calculate_index(start_time, end_coordinates_time, end_time, T_list)

        if 'Cecum' in event and not cecum_found:
            cecum_found = True
            cecum_time = float(timestamp)
            landmarks['Cecum'] = calculate_index(cecum_time, end_coordinates_time, end_time, T_list)

        if 'Fleksur L' in event and not cecum_found:
            flexur_L_time = float(timestamp)
            landmarks['Fleksur L'] = calculate_index(flexur_L_time, end_coordinates_time, end_time, T_list)

        if 'Fleksur R' in event and not cecum_found:
            flexur_R_time = float(timestamp)
            landmarks['Fleksur R'] = calculate_index(flexur_R_time, end_coordinates_time, end_time, T_list)

        if 'Recording ended' in event or 'Endoscopy ended' in event:
            end_time_event = float(timestamp)
            landmarks['End'] = calculate_index(end_time_event, end_coordinates_time, end_time, T_list)

    return (landmarks['Cecum'], landmarks['Fleksur L'], landmarks['Fleksur R'], landmarks['End'], landmarks['Start'])


def get_event_indexes(path, T_list):
    """
    Process a log file and return the indexes of specific events ('Flush', 'Biopsy', 'Polyp', 'Polypectomi').

    Parameters:
    path (str): The directory path containing the log file.
    T_list (list): A list of time coordinates.

    Returns:
    list: A list of lists where each sublist contains the event name and the corresponding indexes in T_list.
    """

    def calculate_event_index(event_time, end_coordinates_time, end_time, T_list):
        """
        Calculate the index of the event closest to the given event_time in T_list.

        Parameters:
        event_time (float): The time of the event.
        end_coordinates_time (float): The last coordinate time in T_list.
        end_time (float): The end time from the log file.
        T_list (list): A list of time coordinates.

        Returns:
        int: The index of the closest time in T_list to the event_time.
        """
        adjusted_time = end_coordinates_time - (end_time - (event_time * 1000))
        closest_value = min(T_list, key=lambda x: abs(x - adjusted_time))
        return T_list.index(closest_value)

    index_path = os.path.join(path, 'LogFile_P.txt')
    event_lists = {
        'Flush': [],
        'Biopsy': [],
        'Polyp': [],
        'Polypectomi': []
    }

    with open(index_path, 'r') as file:
        lines = file.readlines()

    end_coordinates_time = T_list[-1]
    end_time = float(lines[-1].split(';')[0]) * 1000

    for line in lines[1:]:
        timestamp, event = line.split(';')[:2]
        event_time = float(timestamp)

        if event in event_lists:
            event_index = calculate_event_index(event_time, end_coordinates_time, end_time, T_list)
            event_lists[event].append(event_index)
        elif 'Recording ended' in event or 'Endoscopy ended' in event:
            ended_time = end_coordinates_time - (end_time - (event_time * 1000))

    return [[event, indexes] for event, indexes in event_lists.items()]
