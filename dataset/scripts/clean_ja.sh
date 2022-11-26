#! /bin/bash
# Author: Giang Le
# Bash script to apply preprocessing steps to English data.

DIR=$(dirname "$0")
BASE=$DIR/..

while getopts ":c:" opt; do
  case $opt in
  c)
    # Based on SOCKEYE's processing steps:
    echo "Processing $OPTARG data for Japanese" >&2

    awk '{$1=$1;print}' $BASE/data/raw/$OPTARG.ja >$BASE/data/raw/$OPTARG-1.ja

    echo "Removing non printing char"
    cat $BASE/data/raw/$OPTARG-1.ja | $BASE/libraries/moses/scripts/tokenizer/remove-non-printing-char.perl -l ja >$BASE/data/raw/$OPTARG-2.ja

    echo "Normalizing punctuation"
    cat $BASE/data/raw/$OPTARG-2.ja | $BASE/libraries/moses/scripts/tokenizer/normalize-punctuation.perl -l ja >$BASE/data/raw/$OPTARG-cln.ja

    echo "Clean up...."
    rm $BASE/data/raw/$OPTARG-1.ja
    rm $BASE/data/raw/$OPTARG-2.ja
    ;;
  \?)
    echo "Usage: cmd [-c]"
    ;;
  esac
done
