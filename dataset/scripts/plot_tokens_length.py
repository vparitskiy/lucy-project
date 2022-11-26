import os
from pathlib import Path

import mapply
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from transformers import MT5Tokenizer

mapply.init()

lucy_tokenizer = MT5Tokenizer.from_pretrained("../models/lucy-base")

root = Path("./data/raw")

dataframes = []
for src in root.glob("*.en"):
    print(src)
    basename = os.path.basename(src).split(".")[0]
    ja_src = os.path.join(root, basename + ".ja")
    print(ja_src)
    with open(src) as en_file:
        with open(ja_src) as ja_file:
            df = pd.DataFrame.from_dict(
                {
                    "en": en_file.read().split("\n"),
                    "ja": ja_file.read().split("\n"),
                }
            )
    dataframes.append(df)

df = pd.concat(dataframes)
df["en_len"] = [0] * len(df["en"])
df["ja_len"] = [0] * len(df["ja"])

print(df)


def process(row):
    input_ids = lucy_tokenizer.encode(row.en, return_tensors="pt")
    row.en_len = len(input_ids[0])
    input_ids = lucy_tokenizer.encode(row.ja, return_tensors="pt")
    row.ja_len = len(input_ids[0])
    return row


df = df.mapply(process, axis=1)

ja_token_len = df["ja_len"].to_list()
ja_token_len.sort(reverse=True)
plt.figure(figsize=(36, 24), tight_layout=True, dpi=160)
plt.xticks(np.arange(0, 250, 10))
_, _, bars = plt.hist(ja_token_len, bins=range(0, 250, 10))
plt.bar_label(bars)
plt.xlabel("ja token ids length")
plt.ylabel("frequency")
plt.savefig("./data/raw/_tokens_len_ja.jpg")

en_token_len = df["en_len"].to_list()
en_token_len.sort(reverse=True)
plt.figure(figsize=(36, 24), tight_layout=True, dpi=160)
plt.xticks(np.arange(0, 250, 10))
_, _, bars = plt.hist(en_token_len, bins=range(0, 250, 10))
plt.bar_label(bars)
plt.xlabel("en token ids length")
plt.ylabel("frequency")
plt.savefig("./data/raw/_tokens_len_en.jpg")
