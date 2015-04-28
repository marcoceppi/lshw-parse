#!/usr/bin/env python

import json
from parse import Profile

with open('output.sample') as f:
    a = json.loads(f.read())

prof = Profile(a)

for k in sorted(prof.hardware.keys()):
  print("%s: %s" % (k, prof.hardware[k]))

print(json.dumps(prof.packages, indent=2))
