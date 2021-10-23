#!/usr/bin/env bash

CDXAPI="http://web.archive.org/cdx/search/cdx"

while read -r line
do
  idx=$(curl -sG -d "fl=timestamp,statuscode,urlkey" -d "limit=1" --data-urlencode "url=$line" $CDXAPI)
  idx="${idx:=- - -}"
  echo "$line ${idx/*Blocked Site Error/X X X}"
done < <(cat "$@")
