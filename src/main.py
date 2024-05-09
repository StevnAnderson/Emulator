import sys
import re
if len(sys.argv) < 2:
    print("Please specify a file to run")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    lines = f.readlines()

lines = [l.split(';')[0] for l in lines if l.split(';')[0].strip()]
dataSection = True
for l in lines:
    print(l)