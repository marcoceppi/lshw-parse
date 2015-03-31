#!/usr/bin/env python

import json
from parse import Hardware

with open('output.sample') as f:
    a = json.loads(f.read())

h = Hardware(a['lshw'])

for l in h.display():
    print(l)

