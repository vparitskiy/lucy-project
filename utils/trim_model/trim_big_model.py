import torch
from transformers import MT5ForConditionalGeneration
from transformers import MT5Tokenizer


src = "../../models/lucy-toc-131072"
dest = "../../models/lucy_small"
base_src = "../../models/mt5-small"


mt5_toc = MT5Tokenizer.from_pretrained(base_src)
model = MT5ForConditionalGeneration.from_pretrained(base_src)

lucy_toc = MT5Tokenizer.from_pretrained(src)

lucy_vocab = lucy_toc.get_vocab()
mt5_vocab = mt5_toc.get_vocab()

kept_ids = []

for k, v in lucy_vocab.items():
    if k in mt5_vocab:
        print("Keep: ", k)
        kept_ids.append((v, mt5_vocab[k]))
new_size = len(lucy_toc)
print("New size: ", new_size)
new_emb = torch.nn.Embedding(new_size, model.shared.embedding_dim)
new_head = torch.nn.Linear(
    in_features=model.lm_head.in_features, out_features=new_size, bias=False
)

for new_id, old_id in kept_ids:
    new_emb.weight.data[new_id] = model.shared.weight.data[old_id]
    new_head.weight.data[new_id] = model.lm_head.weight.data[old_id]

model.shared.weight = new_emb.weight
model.lm_head.weight = new_head.weight
model.config.__dict__["vocab_size"] = new_size
model.config.__dict__["_name_or_path"] = "vparytskyy/lucy-small"

# from sentencepiece import sentencepiece_model_pb2 as model
#
# smp = tokenizer.sp_model.serialized_model_proto()
# m = model.ModelProto()
# m.ParseFromString(smp)
# print("the loaded model has pieces:", len(m.pieces))
# new_pieces = [m.pieces[idx] for idx in kept_ids[: len(m.pieces)]]
# print("the new pieces:", len(new_pieces))
# for i, p in enumerate(new_pieces):
#     m.pieces[i].piece = p.piece
#     m.pieces[i].score = p.score
#     m.pieces[i].type = p.type
# # drop the remaining pieces
# n = len(new_pieces)
# for i in trange(len(m.pieces) - n):
#     m.pieces.pop(len(m.pieces) - 1)
# with open("new_sp.model", "wb") as f:
#     f.write(m.SerializeToString())
# new_tokenizer = MT5Tokenizer("new_sp.model", extra_ids=0)
#
# new_tokenizer.save_pretrained("satou-mt5-streaming")
lucy_toc.save_pretrained(dest)
model.save_pretrained(dest)
