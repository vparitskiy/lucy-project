import torch
from transformers import MT5ForConditionalGeneration
from transformers import MT5Tokenizer


src = "models/lucy-toc-65536"
dest = "models/lucy-base"
base_src = "models/mt5-base"


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

lucy_toc.save_pretrained(dest)
model.save_pretrained(dest)
