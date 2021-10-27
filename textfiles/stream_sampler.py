#!/usr/bin/env python3

from random import random


class StreamSampler():
  def __init__(self, size=10):
    self._size = size
    self._samples = [None] * size
    self._processed = 0

  def toss(self, item):
    quotient, remainder = divmod(self._processed, self._size)
    if random() < 1 / (quotient + 1):
      self._samples[remainder] = item
    self._processed += 1

  def samples(self):
    return filter(lambda s: s is not None, self._samples)


if __name__ == "__main__":
  import argparse
  import fileinput
  import os
  import sys

  ap = argparse.ArgumentParser(description="Sample N lines randomly from the unknown size input stream with adaptive probability.")
  ap.add_argument("-n", "--number", nargs="?", type=int, default=10, help="Number of sample lines (default: 10)")
  ap.add_argument("files", nargs="*", help="Files (plain/gz/bz2) to sample lines from (reads from the STDIN, if empty or '-')")
  args = ap.parse_args()

  if os.isatty(sys.stdin.fileno()) and not args.files:
    ap.print_help(file=sys.stderr)
    sys.exit()

  size = int(args.number)
  ss = StreamSampler(size)

  for line in fileinput.input(files=args.files, mode="rb", openhook=fileinput.hook_compressed):
    ss.toss(line.decode())

  for sample in ss.samples():
    print(sample, end="")
