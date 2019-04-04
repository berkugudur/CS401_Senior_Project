#!/usr/bin/env python
# coding: utf-8

# ### This notebook includes the experiments for cross validation.
# 
# - Standing agent is P1, we are learning P2 (P2 is human player).
# 
# - Some frames will be removed, there are frames that;
#     - Both players standing.
#     - Consecutive ones(If frame's action is same with previous frame, it will be removed).
#     - If we are(P2) in RECOV frame(Since we don't make RECOV frames ourselves).

# ### Importing libraries

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import TensorBoard, ModelCheckpoint
import time
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
import json

# For using core package that located in the two upper folder.
import os,sys
sys.path.append('../../')

from core.json_importer import parse_json_file, parse_all_files
from core.filters import remove_both_standing_frames, remove_same_consecutive_actions, remove_recov_frames
from core.actions import one_hot_encode, decode
from core.preproccessing import Normalizer
from core.helpers import write_file

# Create out file folder if not exists
OUT_FOLDER = 'generated_files'
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

# Open files
training_data = parse_all_files("data/utal/train")

# ### Pre process data
# 
# - In the pre process phase, we remove P2's datas from training set in order to crate labels. Labels are just actions of P2.
# 
# - We make actions one-hot encoding. 
# 
# - One-hot encoding for inputs and labels are not same. For example, Dash action in the input may have encoding [0,1] while Dash action in the label have encoding [0, 0, 1, 0].
# 
# - Integer values normalized. (P1-HP, P2-HP, P1-X, P1-Y, P2-X, P2-Y)
# 
# - After pre-process we just have <font color='red'>[P1-Action, P1-HP, P2-HP, P1-X, P1-Y, P2-X, P2-Y] -> P2-Action</font>

# #### Remove unneeded frames

# Apply filters for training data
tr_deleted = training_data.filter(remove_both_standing_frames)
tr_deleted += training_data.filter(remove_recov_frames)
tr_deleted += training_data.filter(remove_same_consecutive_actions)


# #### Encoding and normalization
def normalize_and_save(data, file_name):
    p1_hp_normalizer = Normalizer()
    p1_normalized_hp = p1_hp_normalizer.normalize(data)
    p1_hp_normalizer.save(OUT_FOLDER + '/' + file_name)
    return p1_normalized_hp

def process_data(game_data_obj):
    ## Pre process data
    processed_data = []

    # Create one hot encoding for actions (For input and labels)
    p1_one_hot_encoded_actions = one_hot_encode(game_data_obj.get_column("P1-action"))
    labels = one_hot_encode(game_data_obj.get_column("P2-action"))

    # Normalize uncategorized features
    normalized_xp1_distance = normalize_and_save([frame["P1-x"] for frame in game_data_obj], "xp1_norm.save")
    normalized_xp2_distance = normalize_and_save([frame["P2-x"] for frame in game_data_obj], "xp2_norm.save")
    normalized_yp1_distance = normalize_and_save([frame["P1-y"] for frame in game_data_obj], "yp1_norm.save")
    normalized_yp2_distance = normalize_and_save([frame["P2-y"] for frame in game_data_obj], "yp2_norm.save")

    for index in range(len(game_data_obj)):    
        processed_row = []
        processed_row.extend(p1_one_hot_encoded_actions[index])
        processed_row.extend(normalized_xp1_distance[index])
        processed_row.extend(normalized_xp2_distance[index])
        processed_row.extend(normalized_yp1_distance[index])
        processed_row.extend(normalized_yp2_distance[index])
        processed_data.append(processed_row)
    processed_data = np.array(processed_data)
    labels = np.array(labels)
    
    return processed_data, labels
   
tr_data, tr_labels = process_data(training_data)


# ### Neural Network Design
# 
# Our neural network has two hidden layers in this test. They has 12 and 8 neurons respectively.

# Constants
INPUT_LAYER_SIZE = tr_data.shape[1]
OUTPUT_LAYER_SIZE = tr_labels.shape[1]

def create_model(neuron_count):
    model = Sequential()
    model.add(Dense(neuron_count, input_dim=INPUT_LAYER_SIZE, activation='relu'))
    model.add(Dense(OUTPUT_LAYER_SIZE, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

COMPLEXITIES = [10, 25, 50, 100, 150, 250, 500, 750, 1000, 1500, 2500]
EPOCH = 500
BATCH = 32

if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

# Create session folder.
SESSION_FOLDER = OUT_FOLDER + '/session_{}'.format(time.time())

os.makedirs(SESSION_FOLDER)
os.makedirs(SESSION_FOLDER + '/models')
os.makedirs(SESSION_FOLDER + '/logs')
os.makedirs(SESSION_FOLDER + '/histories')

histories = []
# Create and run networks
for complexity in COMPLEXITIES:
    starting_time = time.clock()
    file_name = str(complexity)
    
    model = create_model(complexity)
    print('Model created with {} index.'.format(complexity))
    
    # Logging for tensorboard
    tensorboard = TensorBoard(log_dir= SESSION_FOLDER + "/logs/log_{}".format(file_name))

    # Checkpoint for model save
    checkpoint = ModelCheckpoint(filepath=SESSION_FOLDER + "/model_{}.h5".format(file_name), save_best_only=True, verbose=0)
    
    print('\tTraining started.')
    history = model.fit(tr_data, tr_labels, epochs=EPOCH, validation_split=0.2,
                    shuffle=True, batch_size=BATCH, callbacks=[tensorboard, checkpoint])
    print('\tTraining ended.')

    time_taken = (time.clock() - starting_time) * 1000.0
    
    model_info = {
        'info': 'One hidden layer ANN with {} neurons'.format(complexity),
        'epoch': EPOCH,
        'batch': BATCH,
        'time_taken': time_taken
    }
    
    # Save model and history
    write_file(SESSION_FOLDER + '/models/config_{}.json'.format(file_name), model.to_json())
    write_file(SESSION_FOLDER + '/models/info_{}.json'.format(file_name), json.dumps(model_info))
    
    pickle.dump(history, open(SESSION_FOLDER + '/histories/history_{}.save'.format(file_name), 'wb'))
    
    histories.append(history)
    
    
print('Session completed successfully. {} networks created and their data saved.'.format(len(COMPLEXITIES)))




