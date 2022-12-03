#! /bin/bash
# Author: Giang Le
# Bash script to apply preprocessing steps to English data.

DIR=`dirname "$0"`
BASE=$DIR/..

cat $BASE/dataset/data/raw/*.en > en.txt
cat $BASE/dataset/data/raw/*.ja > ja.txt
#sed -n -e '5000000,5000000 p' -e '5000000q' $BASE/dataset/data/corpus/ja.txt >> ja.txt
sh moses_ja.sh
python mecab_ja.py
sh moses_en.sh

mv en-tok.txt ./dataset/en.txt
mv ja-tok.txt ./dataset/ja.txt

