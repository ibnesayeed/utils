#!/usr/bin/env python3

import fileinput
import sys

from surt import surt

for line in fileinput.input():
  try:
    print(surt(line.strip()))
  except BrokenPipeError:
    break
  except Exception as e:
    print(line, file=sys.stderr)
