#!/usr/bin/env python3

import sys
from random import randrange


class RandomLines():
  def __init__(self, fname):
    self._fname = fname

  def __enter__(self):
    self._file = open(self._fname)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self._file.close()

  def __iter__(self):
    self._size = self._file.seek(0, 2)
    return self

  def __next__(self):
    try:
      self._file.seek(randrange(self._size))
      self._file.readline()
      if self._file.tell() == self._size:
        self._file.seek(0)
      return self._file.readline()
    except:
      raise StopIteration


if __name__ == "__main__":
  with RandomLines(sys.argv[1]) as rl:
    for line in rl:
      try:
        print(line, end="")
      except:
        break
