#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from transformers import MT5Tokenizer

sys.path.append(str(Path(__file__).parent.parent.parent))

from utils.unicode import range_ja
from utils.normalize_text import normalize_en, normalize_ja

tqdm.pandas()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input",
    type=str,
    required=True,
)
args = parser.parse_args()


max_ja_token_length = 128
max_en_token_length = 128


def maketrans(f: str, t: str):
    return {ord(x): ord(y) for x, y in zip(f, t)}


def restore_punctuation(s):
    return s.translate(
        maketrans(
            "!\"#$%&'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣",
            "！”＃＄％＆’（）＊＋，－。／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」",
        ),
    )


def remove_parentless(s, ranges):
    reg = r" ?\([{0} ]*\) ?| ?\（[{0} ]*\） ?| ?「[{0} ]*」 ?| ?『[{0} ]*』 ?".format(ranges)
    s = re.sub(reg, "", s)
    return s


re_find_ja = re.compile(r"[{}]".format(range_ja), re.UNICODE)


def clean_ja_line(s):
    s = normalize_ja(s)
    s = remove_parentless(s, r"a-zA-Z!\?\.,'\"\-— ")
    if not re.findall(re_find_ja, s):
        print(f"Drop: {s}.\n Not a Japanese text.")
        return ""
    return s


def clean_en_line(s):
    s = normalize_en(s)
    s = remove_parentless(s, r"{}!\?\.,'\"\-— ".format(range_ja))
    s = re.sub(re_find_ja, "", s)
    if re.findall(re_find_ja, s):
        print(f"Drop: {s}.\n Japanese found in English")
        return ""
    return s


lucy = MT5Tokenizer.from_pretrained("../models/lucy-base")


def len_diff(n1, n2):
    mx = max([n1, n2])
    mn = min([n1, n2])
    if mx == mn:
        return 0
    try:
        return (abs(mx - mn) / mn) * 100.0
    except ZeroDivisionError:
        return 1000


model = SentenceTransformer(f"../models/all-MiniLM-L12-v2")


def sem_score(sentence1, sentence2) -> float:
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    return torch.diag(cosine_scores).cpu().numpy()[0].astype(float)


def jaccard_score(sentence1, sentence2) -> float:
    a = set(int(i) for i in sentence1)
    b = set(int(i) for i in sentence2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def both_valid(line_en, line_ja):
    encoded_en = lucy.encode(line_en.lower(), return_tensors="pt")[0]
    encoded_ja = lucy.encode(line_ja.lower(), return_tensors="pt")[0]

    len_en = len(encoded_en)
    len_ja = len(encoded_ja)

    if len_en <= 1 or len_ja <= 1:
        print(f"Drop: {line_ja} => {line_en}.\nToo short: {len_ja}/{len_en}")
        return False

    if len_en > max_en_token_length or len_ja > max_ja_token_length:
        print(f"Drop: {line_ja} => {line_en}.\nToo long: {len_ja}/{len_en}")
        return False

    if len_diff(len_en, len_ja) > 500:
        print(f"Drop: {line_ja} => {line_en}.\nDifference in length: {len_diff(len_en, len_ja)}")
        return False

    score = jaccard_score(encoded_en, encoded_ja)
    if score > 0.85:
        print(f"Drop: {line_ja} => {line_en}.\nSimilarity score: {score}")
        return False
    return True


def preprocess(row):
    row.en = clean_en_line(row.en)
    row.ja = clean_ja_line(row.ja)
    if row.en and row.ja and both_valid(row.en, row.ja):
        return row


en_in = "data/raw/" + args.input + ".en"
ja_in = "data/raw/" + args.input + ".ja"
ja_out = "data/preprocessed/" + args.input + ".ja"
en_out = "data/preprocessed/" + args.input + ".en"

with open(ja_in) as ja_in_f:
    with open(en_in) as en_in_f:
        df = pd.DataFrame.from_dict({"en": en_in_f.read().split("\n"), "ja": ja_in_f.read().split("\n")})

        print(df)

        df["en"] = df["en"].astype("string")
        df["ja"] = df["ja"].astype("string")

        df = df.drop_duplicates().query("en != ja").query("en != ''").query("ja != ''")

        print(df)

        # df = df.mapply(preprocess, axis=1)
        df = df.progress_apply(preprocess, axis=1)

        df = df.dropna()

        print(df)

        np.savetxt(en_out, df["en"].values, fmt="%s")
        np.savetxt(ja_out, df["ja"].values, fmt="%s")

print("Done normalizing dataset!")
