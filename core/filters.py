from core.actions import ACTION_MAP

# These are filter methods. They are responsible for removing unnecessary frames from game data.

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
        return prepared_frames;
    
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
            prev_frame = frame_data
        return prepared_frames
    
    return init(frames)