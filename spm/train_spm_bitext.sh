#        base    large   base-mt5
# sizes: 65536  131072   250112
# -100 special tokens
# sizes: 65436  130972   250012
# half:  32718  65486    125006
spm_train --input=dataset/ja-en.txt,dataset/ja-en.small.txt \
  --vocab_size=250112 \
  --accept_language=en,ja \
  --character_coverage=0.997 \
  --split_digits=true \
  --input_sentence_size=20000000 \
  --max_sentence_length=999999999 \
  --train_extremely_large_corpus \
  --shuffle_input_sentence=true \
  --model_prefix=./lucy-toc-250112/spiece \
  --byte_fallback \
  --bos_id=-1 --pad_id=0 --eos_id=1 --unk_id=2

