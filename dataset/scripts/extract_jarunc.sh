#! /bin/bash
DIR=$(dirname "$0")
BASE=$DIR/..
JARUNC_PATH="$BASE"/data/corpus/JaRuNC/en-ja

cat "$JARUNC_PATH"/train.ja "$JARUNC_PATH"/test.ja "$JARUNC_PATH"/dev.ja > "$BASE"/data/raw/jarunc.ja
echo "Total sents count for Japanese: $(wc -l "$BASE"/data/raw/jarunc.ja)"
cat "$JARUNC_PATH"/train.en "$JARUNC_PATH"/test.en "$JARUNC_PATH"/dev.en > "$BASE"/data/raw/jarunc.en
echo "Total sents count for Japanese: $(wc -l "$BASE"/data/raw/jarunc.en)"