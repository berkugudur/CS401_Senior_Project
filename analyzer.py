import sys

expected_args = ["file", "source-file", "target-file"]

if len(sys.argv) != len(expected_args):
    print "ERROR:",
    for arg in expected_args:
        print "[" + arg + "]",
    sys.exit(0)

args = dict(zip(expected_args, sys.argv))