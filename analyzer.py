import os, sys, csv, json

# Helper functions
def get_action_type_map():
    type_map = dict()
    for row in csv.reader(open("data/ActionTypes.csv")):
        type_map.setdefault(row[1], [])
        type_map[row[1]].append(row[0])
    return type_map

def get_args():
    if len(sys.argv) < len(EXPECTED_ARGS):
        print("You have to provide source file in format *.json")
        sys.exit(1)
    return dict(zip(EXPECTED_ARGS, sys.argv))

def convert_dif_x_to_category(x):
    if x <= 0:
        x = -x
    x = x / 50
    return x

def get_player_values(player_data):
    values = []
    for value in PRINTABLE_VALUES:
        values.append(player_data[value])
    return values

# Filter functions
# Check is both players are standing
def is_both_players_stand(frame_data):
    return frame_data["P1"]["action"] in STAND_ACTIONS and frame_data["P2"]["action"] in STAND_ACTIONS

# Remove frames that both players are standing
def remove_both_standing_frames(round_data):
    prepared_frames = []
    for frame_data in round_data:
        if not is_both_players_stand(frame_data):
            prepared_frames.append(frame_data)
    return prepared_frames;

# Check current frame's action is different than prev frame's action for learning player
def is_same_action_with_prev_frame(prev_frame, current_frame):
    return prev_frame[PLAYER_TO_LEARN]["action"] == current_frame[PLAYER_TO_LEARN]["action"]

# Remove consetucive frames that have same actions from learning player
def remove_same_consecutive_actions(round_data):
    prepared_frames = [round_data[0]]
    prev_frame = round_data[0]
    for current_frame in round_data:
        if not is_same_action_with_prev_frame(prev_frame, current_frame):
            prepared_frames.append(current_frame)
        prev_frame = current_frame
    return prepared_frames

# Check current frame's action is recov or base for learning player
def is_recov_frame(frame_data):
    return frame_data[PLAYER_TO_LEARN]["action"] in ACTION_MAP["RECOV"] + ACTION_MAP["BASE"]

# Remove recov actions from learning player
def remove_recov_frames(round_data):
    prepared_frames = []
    for frame_data in round_data:
        if not is_recov_frame(frame_data):
            prepared_frames.append(frame_data)
        prev_frame = frame_data
    return prepared_frames

# Write json round_data to csv file
def write_round(frames, writer):
    # Traverse each frame
    for frame_data in frames:
        frame_count = [str(frame_data["current_frame"])]
        player1_data = get_player_values(frame_data["P1"])
        player2_data = get_player_values(frame_data["P2"])
        # Write frame to csv
        writer.writerow(frame_count + player1_data + player2_data)
        
## Constants
EXPECTED_ARGS = ["file", "source-file"]
PRINTABLE_VALUES = ["action", "hp", "x", "y"]
PLAYER_TO_LEARN = "P2"
STAND_ACTIONS = ["STAND", "STAND_B", "STAND_FB"]
ACTION_MAP = get_action_type_map()
ARGS = get_args()

if __name__ == "__main__":
    try:
        f = open(ARGS["source-file"], "r")
    except FileNotFoundError:
        print("Source file not found.")
        sys.exit(1)

    data = json.load(f)
    first_round = data["rounds"][0]
    
    source_file_name = os.path.basename(ARGS["source-file"]).split(".")[0]
    data_folder = "out/"

    # Create untouched csv
    out_file_path = data_folder + "untouched_" + source_file_name + ".csv"
    writer = csv.writer(open(out_file_path, "w"), delimiter=',')
    write_round(first_round, writer)

    # Remove frames that both player standing and write csv
    standing_actions_removed_round = remove_both_standing_frames(first_round)
    out_file_path = data_folder + "standing_removed_" + source_file_name + ".csv"
    writer = csv.writer(open(out_file_path, "w"), delimiter=',')
    write_round(standing_actions_removed_round, writer)

    # Remove frames that has consecutive same actions write csv
    consecutive_actions_removed_round = remove_same_consecutive_actions(standing_actions_removed_round)
    out_file_path = data_folder + "standing_consecutive_removed_" + source_file_name + ".csv"
    writer = csv.writer(open(out_file_path, "w"), delimiter=',')
    write_round(consecutive_actions_removed_round, writer)

    # Remove frames that both player standing and learning player is recovering and write csv
    recov_actions_removed_round = remove_recov_frames(consecutive_actions_removed_round)
    out_file_path = data_folder + "standing_consecutive_recov_removed_" + source_file_name + ".csv"
    writer = csv.writer(open(out_file_path, "w"), delimiter=',')
    write_round(recov_actions_removed_round, writer)
