import json
import sys

expected_args = ["file", "source-file", "target-file"]
printable_values = ["action", "state", "hp", "x", "y"]

if len(sys.argv) != len(expected_args):
    print "ERROR:",
    for arg in expected_args:
        print "[" + arg + "]",
    sys.exit(0)

args = dict(zip(expected_args, sys.argv))


# def functions

def print_player_values(player_data):
    line = ""
    for value in printable_values:
        line += str(player_data[value]) + ","
    return line[:-1]


def print_frame(frame_data):
    print str(frame_data["current_frame"]) + "," + print_player_values(frame_data["P1"]) + "," + print_player_values(
        frame_data["P2"])


def print_round(round_data):
    for frame_data in round_data:
        print_frame(frame_data)


# end of functions

with open(args["source-file"], "r") as source:
    data_ = json.load(source)

for round_data in data_["rounds"]:
    print_round(round_data)
