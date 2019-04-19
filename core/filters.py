from core.actions import ACTION_MAP

# These are filter methods. They are responsible for removing unnecessary frames from game data.

def remove_unpressed_frames(colums, frames):
    # Check if player pressed any key
    def is_pressed(frame_data):
        key_a = frame_data[colums.index("P2-key_a")]
        key_b = frame_data[colums.index("P2-key_b")]
        key_c = frame_data[colums.index("P2-key_c")]
        key_u = frame_data[colums.index("P2-key_up")]
        key_d = frame_data[colums.index("P2-key_down")]
        key_l = frame_data[colums.index("P2-key_left")]
        key_r = frame_data[colums.index("P2-key_right")]
        return key_a or key_b or key_c or key_u or key_d or key_l or key_r

    # Remove frames that unpressed by player
    def init(round_data):
        prepared_frames = []
        for frame_data in round_data:
            if is_pressed(frame_data):
                prepared_frames.append(frame_data)
        return prepared_frames

    return init(frames)

def remove_both_standing_frames(columns, frames):
    # Check is both players are standing
    def is_both_players_stand(frame_data):
        STAND_ACTIONS = ["STAND", "STAND_B", "STAND_FB"]
        return frame_data[columns.index("P1-action")] in STAND_ACTIONS and frame_data[columns.index("P2-action")] in STAND_ACTIONS

    # Remove frames that both players are standing
    def init(round_data):
        prepared_frames = []
        for frame_data in round_data:
            if not is_both_players_stand(frame_data):
                prepared_frames.append(frame_data)
        return prepared_frames
    
    return init(frames)

def remove_same_consecutive_actions(columns, frames):
    # Check current frame's action is different than prev frame's action for learning player
    def is_same_action_with_prev_frame(prev_frame, current_frame):
        return prev_frame[columns.index("P2-action")] == current_frame[columns.index("P2-action")]

    # Remove consetucive frames that have same actions from learning player
    def init(round_data):
        prepared_frames = [round_data[0]]
        prev_frame = round_data[0]
        for current_frame in round_data:
            if not is_same_action_with_prev_frame(prev_frame, current_frame):
                prepared_frames.append(current_frame)
            prev_frame = current_frame
        return prepared_frames
    
    return init(frames)

def remove_unchange_hp(columns, frames):
    # Check current frame's action is different than prev frame's action for learning player
    def is_hp_change(prev_frame, current_frame):
        return prev_frame[columns.index("P1-hp")] != current_frame[columns.index("P1-hp")] or prev_frame[columns.index("P2-hp")] != current_frame[columns.index("P2-hp")]

    # Remove consetucive frames that have same actions from learning player
    def init(round_data):
        prepared_frames = []
        prev_frame = round_data[0]
        for current_frame in round_data:
            if is_hp_change(prev_frame, current_frame):
                prepared_frames.append(prev_frame)
                prepared_frames.append(current_frame)
            prev_frame = current_frame
        return prepared_frames
    
    return init(frames)

def remove_recov_frames(columns, frames):
    # Check current frame's action is recov or base for learning player
    def is_recov_frame(frame_data):
        return frame_data[columns.index("P2-action")] in ACTION_MAP["RECOV"] + ACTION_MAP["BASE"]

    # Remove recov actions from learning player
    def init(round_data):
        prepared_frames = []
        for frame_data in round_data:
            if not is_recov_frame(frame_data):
                prepared_frames.append(frame_data)
        return prepared_frames
    
    return init(frames)