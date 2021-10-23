#!/usr/bin/env python3

import fileinput
import requests
import sys

from datetime import datetime


def time_diff(dt, cm):
  dtts = datetime.strptime(dt, "%Y%m%d%H%M%S").timestamp()
  cmts = datetime.strptime(cm, "%Y%m%d%H%M%S").timestamp()
  return int(cmts - dtts)


for line in fileinput.input():
  try:
    dt, _, uri = line.strip().partition(" ")
    r = requests.get(f"https://web.archive.org/web/{dt}/{uri}", allow_redirects=False)
    diff = "~"
    if "Memento-Datetime" in r.headers:
      diff = 0
    elif r.status_code == 302:
      cm = r.headers.get("Location").split("/")[4]
      if cm != "_embed":
        diff = time_diff(dt, cm)
    print(f"{uri} {diff}")
  except BrokenPipeError:
    break
  except Exception as e:
    print(line, file=sys.stderr)
