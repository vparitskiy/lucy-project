#! /bin/bash
# Author: Giang Le
# Bash script to apply preprocessing steps to English data.

DIR=`dirname "$0"`
BASE=$DIR/..

while getopts ":c:" opt; do
  case $opt in
    c)
      # Based on SOCKEYE's processing steps:
      echo "Processing $OPTARG data for English" >&2

      awk '{$1=$1;print}' $BASE/data/raw/$OPTARG.en > $BASE/data/raw/$OPTARG-1.en

      echo "Removing non printing char"
      cat $BASE/data/raw/$OPTARG-1.en | $BASE/libraries/moses/scripts/tokenizer/remove-non-printing-char.perl -l en > $BASE/data/raw/$OPTARG-2.en

      echo "Normalizing punctuation"
      cat $BASE/data/raw/$OPTARG-2.en | $BASE/libraries/moses/scripts/tokenizer/normalize-punctuation.perl -l en > $BASE/data/raw/$OPTARG-cln.en

      echo "Clean up...."
      rm $BASE/data/raw/$OPTARG-1.en
      rm $BASE/data/raw/$OPTARG-2.en
      ;;
    \?)
      echo "Usage: cmd [-c]"
      echo "Option for data preprocessing is wmt2021-bitext"
      ;;
  esac
done
