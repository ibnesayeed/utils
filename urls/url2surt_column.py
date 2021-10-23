#!/usr/bin/env python3

import fileinput
import re
import sys
import os

from surt import surt

column = int(os.getenv("COLUMN", 1))
pos = 2 * (column - 1)

for line in fileinput.input():
  try:
    parts = re.split(r"(\s)", line.strip())
    parts[pos] = surt(parts[pos])
    print("".join(parts))
  except BrokenPipeError:
    break
  except Exception as e:
    print(line, file=sys.stderr)
