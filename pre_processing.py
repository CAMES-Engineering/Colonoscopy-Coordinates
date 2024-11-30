



'''
READ THIS !!

This code serves as pseudo-code examples for how raw data was pre-processed before publishing. We say pseudo code, as functions are redacted if they contain hard-coded information on the devices uses.e.g. indices for looping sensors or similar.

Functions changes are marked with 

    !!!!!!!!!
    REDACTED
    !!!!!!!!!



'''






import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import string
import shutil 
import json


def generate_random_string(length=12):
    """Generate a random string of given length including letters and digits."""
    characters = string.ascii_letters + string.digits  
    return ''.join(random.choices(characters, k=length))


def running_average(data, window_size):
    """
    Compute the running average of a 1D numpy array using a specified window size.
    """
    # Create a window: an array of ones divided by the window size
    window = np.ones(window_size) / window_size
    
    # Compute the convolution, which applies the running average
    running_avg = np.convolve(data, window, mode='same')
    
    return running_avg


def load_coordinates_raw(filepath):
    """
    Read csv file, return numpy array.
    """
    datalines = []
    i = 0
    with open(filepath, "r") as f:
        for line in f.readlines():
            if i > 0:
                datalines.append(line.split(",")[:-1])
            i += 1
    return np.array(datalines)


def parse_time(timestr):
    """Parse a time string into a datetime object."""
    return datetime.datetime.strptime(timestr, '%H:%M:%S:%f')


def calculate_relative_time(data):
    """
    Convert array timestamps to relative times in milliseconds and handle type issues.
    """
    modified_data = []
    first_time = parse_time(data[0][0])
    
    for row in data:
        current_time = parse_time(row[0])
        time_diff = (current_time - first_time).total_seconds() * 1000
        new_row = [str(time_diff)] + [str(item) for item in row[1:]]
        modified_data.append(new_row)
    
    return np.array(modified_data)  


def extract_columns(data, N):
    """
    !!!!!!!!!
    REDACTED
    !!!!!!!!!

    Extract specific columns from the data array up to column N.

    """
    selected_indices = ------REDACTED------

    # Filter the data to only include the selected columns
    modified_data = []
    for row in data:
        new_row = [float(row[i]) for i in ------REDACTED------]
        modified_data.append(new_row)
    
    return np.array(modified_data)


def coiler(data, scale_factor, translation_offset):
    """Apply a linear transformation"""
    transformed_data = []

    for row in data:
        new_row = []
        new_row.append(------REDACTED------)
        coordinates = np.array(------REDACTED------, dtype=float)
        
        scaled = coordinates * scale_factor
        
        transformed = scaled + translation_offset
        new_row.extend([float(f"{coord:.2f}") for coord in transformed])
        transformed_data.append(new_row)

    return np.array(transformed_data)


def data_to_shape(data):
    '''
    !!!!!!!!!
    REDACTED
    !!!!!!!!!

    Convert an input data array to a dictionary with structured coordinate data.'''
    output_dict = {}

    # Initialize output dictionary for each coil
    for coil_no in range(---REDACTED---):
        output_dict[coil_no] = {'T': [], 'X': [], 'Y': [], 'Z': []}

    # Process each row
    for row in data:
        timestamp = row[0]
        index = ---REDACTED---
        for coil_no in range(---REDACTED---):
            if ---REDACTED--- < len(row):
                output_dict[coil_no]['T'].append(timestamp)
                output_dict[coil_no]['X'].append(row[---REDACTED---])
                output_dict[coil_no]['Y'].append(row[---REDACTED---])
                output_dict[coil_no]['Z'].append(row[---REDACTED---])
            index += ---REDACTED---  
    return output_dict


def averager_coils(DDD):
    '''

    !!!!!!!!!
    REDACTED
    !!!!!!!!!

    Applies running average to dict.'''
    outd = {}
    for coil_no in range(---REDACTED---):
        outd[coil_no] = {'T': [], 'X': [], 'Y': [], 'Z': []}

    for coil_no in range(---REDACTED---):
        outd[coil_no]["X"] = list(running_average(DDD[coil_no]["X"], ---REDACTED---))
        outd[coil_no]["Y"] = list(running_average(DDD[coil_no]["Y"], ---REDACTED---))
        outd[coil_no]["Z"] = list(running_average(DDD[coil_no]["Z"], ---REDACTED---))
    return outd


def save_animation(datadict, savep):

    !!!!!!!!!
    REDACTED
    !!!!!!!!!

    # Plot setup
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    line, = ax1.plot([], [], 'k-')

    ax1.set_xlim([-250, 250])
    ax1.set_ylim([-250, 250])
    ax1.set_title("XY")

    # Second subplot
    line2, = ax2.plot([], [], 'b-')
    ax2.set_title("ZY")
    ax2.set_ylim([-250, 250])
    ax2.set_xlim([0, 500])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax1.set_yticks([])
    ax1.set_xticks([])

    # Update function for animation
    def update(frame):
        XX = []
        YY = []
        ZZ = []

        for coil_no in range(---REDACTED---):
            XX.append(datadict[coil_no]["X"][frame])
            YY.append(datadict[coil_no]["Y"][frame])
            ZZ.append(datadict[coil_no]["Z"][frame])

        XX = np.array(XX)
        YY = np.array(YY)
        ZZ = np.array(ZZ)

        line.set_data(XX, -np.array(YY))
        line2.set_data(ZZ, -np.array(YY))

        return line, line2

    # Create animation
    ani = FuncAnimation(fig, update, frames=len(datadict[0]["T"]), blit=True, interval=200)

    # Save animation
    ani.save(savep, writer='ffmpeg', fps=5)
    plt.clf()


filepath = "/home/.../IRE/D6_1_COORDINATES_DATA/Unprocessed/SimBatch/... .csv"
outdir = "/home/.../IRE/D6_1_COORDINATES_DATA/Processed_delivery/SimBatch/"
indir = "/home/.../IRE/D6_1_COORDINATES_DATA/Unprocessed/SimBatch/"

# Cleaning
'''
with open("SIMMETA.txt", 'w') as metafile:
    print("reset file")

try:
    shutil.rmtree(outdir)
    os.mkdir(outdir)
except FileNotFoundError:
    os.mkdir(outdir)
'''


for root, dirs, files in os.walk(indir):
    for filename in files:
        if filename.endswith(".csv") and "sensor" in filename:
            random_string = generate_random_string()
            print("\n\n \t \t", filename, root, random_string)
            dst_dir = outdir + os.sep + random_string + os.sep
            os.mkdir(dst_dir)

            dataraw = load_coordinates_raw(root + os.sep + filename)
            data_time_rel = calculate_relative_time(dataraw)
            data_sel_col = extract_columns(data_time_rel, ---REDACTED---)

            data_tf = coiler(data_sel_col, ---REDACTED---, ---REDACTED---)

            data_raw = data_to_shape(data_sel_col)
            data_dict = data_to_shape(data_tf)
            data_avg = averager_coils(data_dict)
            
            for coil_no in range(---REDACTED---):
                data_dict[---REDACTED---]["T"] = list(np.array(---REDACTED---)
                data_avg[---REDACTED---]["T"] = list(np.array(---REDACTED---)

            save_animation(data_avg, dst_dir + "animation.mp4")

            shutil.copy(root + os.sep + "LogFile.txt", dst_dir + os.sep + "LogFile.txt")

            with open("SIMMETA.txt", 'a') as metafile:
                metafile.write(f"{root};{filename};{random_string};{dst_dir};\n")
