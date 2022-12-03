#        base    large   base-mt5
# sizes: 65536  131072   250112
# -100 special tokens
# sizes: 65436  130972   250012
# half   32718  65486    125006
spm_train --input=ja-tok.txt \
  --vocab_size=32718 \
  --accept_language=ja \
  --split_digits=true \
  --input_sentence_size=10000000 \
  --max_sentence_length=999999999 \
  --train_extremely_large_corpus \
  --shuffle_input_sentence=true \
  --model_prefix=lucy-toc-65536/spiece.ja \
  --bos_id=-1 --pad_id=0 --eos_id=1 --unk_id=2

