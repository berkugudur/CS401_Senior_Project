import os, re, json
from core.models import GameData

users = ["P1", "P2"]


def _extract_column_names(json_obj):
    cols = []
    for user in users:
        for col in json_obj["rounds"][0][0][users[0]].keys():
            if col != "projectiles":
                cols.append(user + "-" + col)
    return cols


def parse_json_file(path):
    with open(path, 'r') as f:
        json_obj = json.load(f)
        columns = _extract_column_names(json_obj)
        game = GameData(columns=columns)

        # Traverse each round
        for each_round in json_obj["rounds"]:
            frames = []
            # Traverse each frame
            for each_frame in each_round:
                frame = []
                for col in columns:
                    user = each_frame[col[0:2]]
                    frame.append(user[col[3:len(col)]])
                frames.append(frame)
            game.add_round(frames)

        return game


def parse_all_files(path):
    root = None
    for file_name in os.listdir(path):
        if is_json_file(file_name):
            if not root:
                root = parse_json_file(path + "/" + file_name)
            else:
                root.append(parse_json_file(path + "/" + file_name))
    return root


def is_json_file(file_name):
    tmp = file_name.split(".")
    return "json" == tmp[len(tmp) - 1]
