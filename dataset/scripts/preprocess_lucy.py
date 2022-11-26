import csv
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import MT5Tokenizer

sys.path.append(str(Path(__file__).parent.parent.parent))

from utils.unicode import range_ja

max_ja_token_length = 128
max_en_token_length = 128

tqdm.pandas()

lucy_tokenizer = MT5Tokenizer.from_pretrained("../models/lucy-base")

root = Path(__file__).parent.parent


def validate_ja(s):
    if not re.findall(re_find_ja, s):
        print(f"Drop: {s}.\n Not a Japanese text.")
        return ""
    return s


re_find_ja = re.compile(r"[{}]".format(range_ja), re.UNICODE)


def validate_en(s):
    if re.findall(re_find_ja, s):
        print(f"Drop: {s}.\n Japanese found in English")
        return ""
    return s


def len_diff(n1, n2):
    mx = max([n1, n2])
    mn = min([n1, n2])
    if mx == mn:
        return 0
    try:
        return (abs(mx - mn) / mn) * 100.0
    except ZeroDivisionError:
        return 1000


def jaccard_score(sentence1, sentence2) -> float:
    a = set(int(i) for i in sentence1)
    b = set(int(i) for i in sentence2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def validate(line_en, line_ja):
    encoded_en = lucy_tokenizer.encode(line_en.lower(), return_tensors="pt")[0]
    encoded_ja = lucy_tokenizer.encode(line_ja.lower(), return_tensors="pt")[0]

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
    row.en = validate_en(row.en)
    row.ja = validate_ja(row.ja)
    if validate_en(row.en) and validate_ja(row.ja) and validate(row.en, row.ja):
        return row


with open('data/raw/lucy.ja') as ja_in_f:
    with open('data/raw/lucy.en') as en_in_f:
        df = pd.DataFrame.from_dict({"en": en_in_f.read().split("\n"), "ja": ja_in_f.read().split("\n")})

print(df)

# df = df.mapply(preprocess, axis=1)
df = df.progress_apply(preprocess, axis=1)
df = df.dropna()
print(df)
np.savetxt('data/preprocessed/lucy.en', df["en"].values, fmt="%s")
np.savetxt('data/preprocessed/lucy.ja', df["ja"].values, fmt="%s")
