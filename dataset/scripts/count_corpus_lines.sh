#! /bin/bash

DIR=$(dirname "$0")
BASE=$DIR/..

echo "Lucy pairs:$(wc -l "$BASE"/data/corpus/lucy/*.csv | tail -n 1)"
echo "Total pairs:$(wc -l "$BASE"/data/preprocessed/*.ja | tail -n 1)"
