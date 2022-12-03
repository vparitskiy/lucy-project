#! /bin/bash
# Author: Giang Le
# Bash script to apply preprocessing steps to English data.

DIR=`dirname "$0"`
BASE=$DIR/..

# Based on SOCKEYE's processing steps:
echo "Processing data for Japanese" >&2
echo "Removing non printing char"
cat ja.txt | $BASE/utils/mosesdecoder/scripts/tokenizer/remove-non-printing-char.perl -l ja > ja1.txt
rm ja.txt
mv ja1.txt ja.txt
