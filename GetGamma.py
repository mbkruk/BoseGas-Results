#!/usr/bin/env python3

import sys
import json

with open("findmin/data.json") as f:
	data = json.loads(f.read())

interaction = sys.argv[2]
extra = str(int(sys.argv[1]))

if interaction=="contact":
	gamma = data[interaction][extra]
else:
	width = "{:.3f}".format(float(sys.argv[3]))
	gamma = data[interaction][width][extra]

print(gamma)
