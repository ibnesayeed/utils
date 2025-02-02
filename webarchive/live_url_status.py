#!/usr/bin/env python3

import fileinput
import requests
import socket
import sys
import urllib3


def check_http_status(url, maxrdr=10, tout=(10, 30)):
  """
  Checks the HTTP status of a URL and provides details.

  Args:
    url: The URL to check.

  Returns:
    A tuple containing:
      - Verbal status
      - Number of redirects
      - The initial status code
      - The final status code
      - The original URL
      - The final URL after any redirects
  """
  ses = requests.Session()
  ses.max_redirects = maxrdr

  rdrct = 0
  finurl = "-"
  initst = -1

  try:
    res = ses.get(url, timeout=tout, allow_redirects=True)
    rdrct = len(res.history)
    vst = res.reason.replace(" ", "_")
    finst = res.status_code
    finurl = res.url
    initst = res.history[0].status_code if res.history else finst
  except requests.exceptions.TooManyRedirects as e:
    res = ses.get(url, timeout=tout, allow_redirects=False)
    rdrct = -1
    vst = "Too_Many_Redirects"
    finst = -3
    initst = res.status_code
  except requests.exceptions.Timeout as e:
    vst = "Timeout"
    finst = -2
  except requests.exceptions.ConnectionError as e:
    vst = "Connection_Error"
    finst = -1

  return vst or finst, rdrct, initst, finst, url, finurl


def main():
  for line in fileinput.input():
    url = line.strip()
    try:
      urlst = check_http_status(url)
      print("\t".join([str(i) for i in urlst]))
    except (BrokenPipeError, KeyboardInterrupt):
      break
    except Exception as e:
      print(f"{url}\t{e}", file=sys.stderr)


if __name__ == "__main__":
  main()
