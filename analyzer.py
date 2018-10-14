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


# def functions

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


# end of functions

data_ = json.load(open(args["source-file"], "r"))
writer_ = csv.writer(open(args["target-file"], "w"), delimiter=',')

for round_data in data_["rounds"]:
    write_round(round_data, writer_)
