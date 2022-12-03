#! /bin/bash
# Author: Giang Le
# Bash script to apply preprocessing steps to English data.

DIR=`dirname "$0"`
BASE=$DIR/..


# Based on SOCKEYE's processing steps:
echo "Processing $OPTARG data for English" >&2
echo "Normalizing punctuation"
cat en.txt | $BASE/utils/mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l en > en-punc-normalized.txt
echo "Removing non printing char"
cat en-punc-normalized.txt | $BASE/utils/mosesdecoder/scripts/tokenizer/remove-non-printing-char.perl -l en > en-punc-normalized1.txt
echo "Tokenizing English data"
cat en-punc-normalized1.txt | $BASE/utils/mosesdecoder/scripts/tokenizer/tokenizer.perl -no-escape -l en -threads 8 -protected=$BASE/utils/mosesdecoder/scripts/tokenizer/basic-protected-patterns > en-tok.txt
echo "LINES COUNT CHECK - PARALLEL LC MUST BE EQUAL!"
echo "##############################################"
echo "$(wc -l en-tok.txt)"
echo "$(wc -l ja-tok.txt)"
echo "##############################################" 
echo "Clean up...."
rm en-punc-normalized.txt
rm en-punc-normalized1.txt
