import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_credentials():
    # Paths to the CSV file and the key file
    csv_file_path = os.path.join(dir_path, 'database/key_info/accounts.csv')
    key_file_path = os.path.join(dir_path, 'database/key_info/key.txt')

    # Read the current key from the key file
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as file:
            key_num = int(file.read().strip())
    else:
        # If the key file does not exist, set a default key (e.g., 1)
        key_num = 1
    # Read the CSV file and assign the values
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['key']) == key_num:
                return row['id'], row['secret']

    # Handle the case where the key is not found
    raise ValueError("Key not found in the CSV file")

def update_key():
    key_file_path = os.path.join(dir_path, 'database/key_info/key.txt')

    # Check if the key file exists and read the last key
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as file:
            last_key = int(file.read().strip())
    else:
        last_key = 0
        print("couldn't find file")

    # Increment the key
    new_key = last_key + 1
    if new_key == 8:
        new_key = 1

    # Update the key file with the new key
    with open(key_file_path, 'w') as file:
        file.write(str(new_key))

def get_current_key():
    key_file_path = os.path.join(dir_path, 'database/key_info/key.txt')

    # Check if the key file exists and read the current key
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as file:
            current_key = int(file.read().strip())
    else:
        # If the file doesn't exist, assume the current key is 1
        current_key = 1
        print("Couldn't find file; get_current_key")

    return current_key

def change_keys(key, secret):
    new_key = update_key()
    get_credentials(key, secret)

def get_keys():
    return get_credentials()


import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def generate_sonic_profile(tracks):
    tracks_df = pd.DataFrame(tracks)
    features = ['tempo', 'danceability', 'valence', 'loudness', 'energy', 'speechiness', 'acousticness', 'popularity']

    # Standardizing and PCA
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(tracks_df[features])
    pca = PCA(n_components=2)
    tracks_reduced = pca.fit_transform(standardized_data)

    # Calculate the average of the transformed tracks (PCA results)
    average_pca = tracks_reduced.mean(axis=0)
    # Scale up the PCA averages to make the small numbers more significant
    scaled_pca = average_pca * 1e16  # Scale up by a factor of 1e15
    max_abs_value = max(abs(scaled_pca))
    if max_abs_value > 1:
        scaled_pca = scaled_pca / max_abs_value

    # Get the x and y values
    x_value, y_value = scaled_pca
    # Rounding the values
    x_value = round(x_value, 5)
    y_value = round(y_value, 5)

    # Averages and variances of original dataset
    component_averages = tracks_df[features].mean()
    component_variances = tracks_df[features].var()
    overall_variance = component_variances.sum()
    variance_scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_variance = variance_scaler.fit_transform([[overall_variance]])[0][0]

    averages = component_averages.to_dict()

    return x_value, y_value, averages, scaled_variance