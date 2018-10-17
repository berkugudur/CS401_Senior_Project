import json
import sys
import csv

# source-file [ *.json ]
# target-file [ *.csv ]
# print [ 1 / 0 ]
expected_args = ["file", "source-file", "target-file", "print"]
printable_values = ["action", "state", "hp", "x", "y"]

if len(sys.argv) < len(expected_args):
    print "ERROR:",
    for arg in expected_args:
        print "[" + arg + "]",
    sys.exit(0)

args = dict(zip(expected_args, sys.argv))
x_as_category = True


# def functions
def convert_dif_x_to_category(x):
    if x <= 0:
        x = -x
    x = x / 50
    return x


def print_player_values(player_data):
    line = ""
    for value in printable_values:
        line += str(player_data[value]) + ","
    return line[:-1]


def get_player_values(player_data):
    values = []
    for value in printable_values:
        values.append(player_data[value])
    return values


def print_frame(frame_data):
    print str(frame_data["current_frame"]) + "," + print_player_values(frame_data["P1"]) + "," + print_player_values(
        frame_data["P2"])


def write_round(round_data, writer):
    for frame_data in round_data:
        writer.writerow([frame_data["current_frame"]] + get_player_values(frame_data["P1"]) + get_player_values(
            frame_data["P2"]))
        if args["print"] == "1":
            print_frame(frame_data)


def write_round_standb(round_data, writer):
    last_data = round_data[0]
    for frame_data in round_data:
        action = get_player_values(frame_data["P1"])[0]
        last_action = get_player_values(last_data["P1"])[0]
        if get_player_values(frame_data["P1"])[0] == "STAND_B" or get_player_values(frame_data["P1"])[0] == "STAND_FB":
            if action != last_action:
                if x_as_category:
                    x_category = convert_dif_x_to_category(
                        get_player_values(frame_data["P1"])[3] - get_player_values(frame_data["P2"])[3])
                else:
                    x_category = get_player_values(frame_data["P1"])[3] - get_player_values(frame_data["P2"])[3]
                writer.writerow([frame_data["current_frame"]] + [get_player_values(frame_data["P1"])[0]] + [
                    get_player_values(frame_data["P2"])[0]] + [x_category])
        if args["print"] == "1":
            print_frame(frame_data)
        last_data = frame_data


def get_action_type_map(reader):
    type_map = dict()
    for row in reader:
        type_map.setdefault(row[1], [])
        type_map[row[1]].append(row[0])
    return type_map


# end of functions

data_ = json.load(open(args["source-file"], "r"))
writer_ = csv.writer(open(args["target-file"], "w"), delimiter=',')
reader_ = csv.reader(open("data/ActionTypes.csv"))

action_type_map = get_action_type_map(reader_)
for round_data in data_["rounds"]:
    write_round(round_data, writer_)
