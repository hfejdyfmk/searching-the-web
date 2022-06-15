#!/bin/sh

main_page="http://shakespeare.mit.edu/"
curl $main_page | grep "a href"  | \
  sed "s/\(<br>\|<em>\|<a href\|\"\)/#/g" | \
  sed "s/\(###\|##\)/#/g" | \
  cut -d "#" -f 3 | \
  sed "s/index\.html/full\.html/g" | \
  while read -r subpage; do
    url="$main_page$subpage"
    fname=$(echo "$subpage" | sed "s#\/#_#g" | cut -d "." -f 1)
    curl "$url" | pandoc -f html -t plain > ./data/$fname.txt
  done
