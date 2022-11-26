#! /bin/bash
# Author: Giang Le
# Write all bitext corpora to data/raw/wmt2021_bitext.{en|ja}

DIR=$(dirname "$0")
BASE=$DIR/..
NAME=lucy-bitext

echo "Concatenate all bitext corpora..."
while getopts ":c:" flag; do
  case $flag in
  c)
    case $OPTARG in
    train/raw | dev/raw | test/raw)
      if [[ -f $BASE/data/$OPTARG/"${NAME}".ja ]]; then
        rm $BASE/data/$OPTARG/"${NAME}".ja
      fi
      if [[ -f $BASE/data/$OPTARG/"${NAME}".en ]]; then
        rm $BASE/data/$OPTARG/"${NAME}".en
      fi
      for corpus in paracrawl anime_subtitles lucy wikimatrix jarunc; do
        cat $BASE/data/$OPTARG/$corpus.ja >>$BASE/data/$OPTARG/"${NAME}".ja
        cat $BASE/data/$OPTARG/$corpus.en >>$BASE/data/$OPTARG/"${NAME}".en
      done
      echo "Total pairs count for bitext data in Japanese: $(wc -l $BASE/data/$OPTARG/"${NAME}".ja)"
      echo "Total pairs count for bitext data in English: $(wc -l $BASE/data/$OPTARG/"${NAME}".en)"
      ;;
    *)
      echo "Invalid argument: $OPTARG. Usage: ./scripts/concatenate_bitext.sh -c train/raw. Argument must be one of train/raw, dev/raw, or test/raw" >&2
      ;;
    esac
    ;;
  \?)
    echo "Invalid option: -$OPTARG. Specify a corpus using a -c flag. Usage: ./scripts/concatenate_bitext.sh -c train/raw. Argument must be one of train/raw, dev/raw, or test/raw" >&2
    exit 1
    ;;
  esac
done
