from sentencepiece import sentencepiece_model_pb2 as spmp
from transformers import MT5Tokenizer

src = "models/lucy-toc-65436"
base_src = "models/mt5-small"

dest = "models/lucy-toc-65536"

lucy_toc = MT5Tokenizer.from_pretrained(src)
base_toc = MT5Tokenizer.from_pretrained(base_src)


lucy_smp = lucy_toc.sp_model.serialized_model_proto()
lucy_m = spmp.ModelProto()
lucy_m.ParseFromString(lucy_smp)

base_smp = base_toc.sp_model.serialized_model_proto()
base_m = spmp.ModelProto()
base_m.ParseFromString(base_smp)

assert len(lucy_m.pieces) == 65436

for piece in base_m.pieces[-100:]:
    new_piece = spmp.ModelProto.SentencePiece(
        piece=piece.piece, score=piece.score, type=piece.type
    )

    lucy_m.pieces.append(new_piece)

assert len(lucy_m.pieces) == 65536

assert lucy_m.pieces[65535].piece == "▁<extra_id_0>"

with open(f"{dest}/spiece.model", "wb") as f:
    f.write(lucy_m.SerializeToString())

tokenizer = MT5Tokenizer(f"{dest}/spiece.model", extra_ids=0)
assert list(tokenizer.get_vocab())[-1] == "▁<extra_id_0>"

tokenizer.save_pretrained(dest)
