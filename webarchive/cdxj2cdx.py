#!/usr/bin/env python3

import fileinput
import json
import sys

for line in fileinput.input():
  try:
    urlkey, datetime, rest = line.strip().split(maxsplit=2)
    j = json.loads(rest)
    print(" ".join([
      urlkey,
      datetime,
      j.get('url', '-'),
      j.get('mime', '-'),
      j.get('status', '-'),
      j.get('digest', '-'),
      j.get('length', '-'),
      j.get('offset', '-'),
      j.get('filename', '-')
    ]))
  except BrokenPipeError:
    break
  except Exception as e:
    print(line, file=sys.stderr)
