#!/usr/bin/env bash

# set -x

CDXAPI="https://web.archive.org/cdx/search/cdx"

usage() {
  cat <<EOM
Download paginated/filtered CDX records from Wayback Machine CDX Server API.
Docs: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server

Usage:
  $0 [OPTIONS] <URL>

Options:
  -m    matchType param (exact [default], prefix, host, domain)
  -o    fl param (comma separated order of FIELDs)
  -f    filter param [repeatable, e.g., !statuscode:200 and mimetype:text/html]
  -c    collapse param (FIELD or FIELD:N) [repeatable]
  -b    begin/from time (YYYY[MM[DD[hh[mm[ss]]]]])
  -e    end/to time (YYYY[MM[DD[hh[mm[ss]]]]])
  -l    limit param (N or -N results)
  -p    pageSize param (default: 5)

Fields:
  urlkey, timestamp, original, mimetype, statuscode, digest, length
EOM
  exit 1
}

match="exact"
pgsz=5

args=()

while getopts ":b:c:e:f:l:m:o:p:" opt
do
  case "$opt" in
    b)
      args+=(-d "from=$OPTARG")
      ;;
    c)
      args+=(-d "collapse=$OPTARG")
      ;;
    e)
      args+=(-d "to=$OPTARG")
      ;;
    f)
      args+=(-d "filter=$OPTARG")
      ;;
    l)
      args+=(-d "limit=$OPTARG")
      ;;
    m)
      match="$OPTARG"
      ;;
    o)
      args+=(-d "fl=$OPTARG")
      ;;
    p)
      pgsz="$OPTARG"
      ;;
    \?)
      usage >&2 && exit 1
      ;;
    :)
      echo "The -$OPTARG option needs a value." >&2 && exit 1
      ;;
  esac
done

shift $((OPTIND-1))

[ -z "$1" ] && usage >&2 && exit 1

url="$1"

args+=(-d "pageSize=$pgsz")
args+=(-d "matchType=$match")

cmd=(curl -sG -d "pageSize=$pgsz" -d "showNumPages=true" -d "matchType=$match" --data-urlencode "url=$url" $CDXAPI)

pages=$("${cmd[@]}")

SECONDS="0"
for p in $(seq 0 $((pages-1)))
do
  curl -sG "${args[@]}" -d "page=$p" --data-urlencode "url=$url" $CDXAPI
  >&2 echo -en "\r[`date -d@${SECONDS} -u +%H:%M:%S`] $((p+1))/$pages"
done

>&2 echo
