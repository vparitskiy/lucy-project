TRAIN_FILES_SRC=dataset/data/train/raw
TRAIN_FILES=$(for SRC in "${TRAIN_FILES_SRC}"/*.{en,ja}; do echo "${SRC}"; done | tr "\n" ",")
LEIPZIG_CORPORA=$(for SRC in ./dataset/data/corpus/Leipzig_Corpora_Collection/*.txt; do echo "${SRC}"; done | tr "\n" ",")

# sizes: 65536  131072
# -100 special tokens
# sizes: 65436  131072
spm_train --input="${TRAIN_FILES}${LEIPZIG_CORPORA}" \
  --vocab_size=65436 \
  --accept_language=en,ja --character_coverage=0.9995 \
  --split_digits=true \
  --input_sentence_size=10000000 \
  --max_sentence_length=999999999 \
  --shuffle_input_sentence=true \
  --model_prefix=models/lucy-toc-65436/spiece \
  --user_defined_symbols_file=dataset/sm/userdef.txt \
  --required_chars_file=dataset/sm/required.txt \
  --byte_fallback \
  --bos_id=-1 --pad_id=0 --eos_id=1 --unk_id=2
