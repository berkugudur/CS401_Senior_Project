import os, sys, csv, json, argparse

# For using core package that located in the one upper folder.
sys.path.append('../../')

from core.json_importer import is_json_file, parse_json_file, parse_all_files
from core.filters import remove_both_standing_frames, remove_same_consecutive_actions, remove_recov_frames

# Initialize parser
parser = argparse.ArgumentParser(description='Converts json files to filtered csv files.')
parser.add_argument('--source', type=str, required=True, help='Input file. It must be json.')
parser.add_argument('--columns', type=str, nargs='+', help='Column names.')
args = parser.parse_args()

# Prepare columns that user wants to see in csv files.
printable_values = args.columns if args.columns else ["P1-action", "P1-hp", "P1-x", "P1-y", "P2-action", "P2-hp", "P2-x", "P2-y"]

# Parse json and create game data object.
try:
    if is_json_file(args.source):
        original_data = parse_json_file(args.source)
    else:
        original_data = parse_all_files(args.source)
except FileNotFoundError:
    print("File '{}' not found.".format(args.source))
    sys.exit(1)

# Create csv files
original_data.export_csv(file_name="untouched", columns=printable_values)

clone = original_data.clone()
clone.filter(remove_both_standing_frames)
clone.export_csv(file_name="standing_removed", columns=printable_values)

clone = original_data.clone()
clone.filter(remove_both_standing_frames)
clone.filter(remove_same_consecutive_actions)
clone.export_csv(file_name="standing_consecutive_removed", columns=printable_values)

clone = original_data.clone()
clone.filter(remove_both_standing_frames)
clone.filter(remove_recov_frames)
clone.export_csv(file_name="standing_recov_removed", columns=printable_values)

clone = original_data.clone()
clone.filter(remove_both_standing_frames)
clone.filter(remove_same_consecutive_actions)
clone.filter(remove_recov_frames)
clone.export_csv(file_name="standing_consecutive_recov_removed", columns=printable_values)

# Info
print("Exporting finished successfully. Csv files can be found in /out.")