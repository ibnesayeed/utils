#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
  sys.exit(f"Patch a file by matching the first columns\n\nUsage:\n  {sys.argv[0]} <orig> <patch>")

with open(sys.argv[1]) as orig, open(sys.argv[2]) as patch:
  for pl in patch:
    pk = pl.split()[0]
    for ol in orig:
      if (ol.split() or [''])[0] == pk:
        sys.stdout.write(pl)
        break
      else:
        sys.stdout.write(ol)
  for ol in orig:
    sys.stdout.write(ol)
