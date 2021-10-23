#!/usr/bin/env python3

import fileinput

for line in fileinput.input():
  try:
    host, rest = line.strip().split(")", 1)
    host = ".".join(reversed(host.strip(",").split(",")))
    print(f"https://{host}{rest or '/'}")
  except BrokenPipeError:
    break
  except:
    print(line, end="")
