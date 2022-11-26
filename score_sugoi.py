import argparse
import csv
import logging
import os.path
import zipfile
from pathlib import Path
from time import sleep

import httpx
import mapply
import pandas as pd
from slugify import slugify
from tqdm import tqdm
from transformers import MT5Tokenizer

logger = logging.getLogger()
from googletrans import Translator

logger.setLevel("ERROR")

root = Path(__file__).parent.parent

os.environ["TOKENIZERS_PARALLELISM"] = "false"

tqdm.pandas()

mapply.init(n_workers=4)


def get_en_tokens_diff(sent1, sent2):
    sent1 = len(set(sent1))
    sent2 = len(set(sent2))

    if sent1 > 10 > sent2:
        mx = max([sent1, sent2])
        mn = min([sent1, sent2])
        if mx == mn:
            return 0
        try:
            return (abs(mx - mn) / mn) * 100.0
        except ZeroDivisionError:
            return 0
    return 0


translator = Translator()

timeout = httpx.Timeout(timeout=50.0)
client = httpx.Client(timeout=timeout)


class BadAlignmentDetector:
    rows = []

    def add(self, row):
        if row.sem_score < 0.2:
            self.rows.append({"ja": row.ja, "en": row.en, "sem_score": row.sem_score, 'sugoi': row.sugoi})
        else:
            self.reset()

    def reset(self):
        if len(self.rows) > 2:
            print(f"Possible unaligned segment:\n")
            for idx, row in enumerate(self.rows):
                print(f"{idx + 1}: {row['ja']} | {row['en']} => {row['sugoi']} | {row['sem_score']}"),
        self.rows = []


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


lucy = MT5Tokenizer.from_pretrained("models/lucy-base")


class RowValidator:
    def is_valid(self, row):
        line_en = row.en.lower()
        line_ja = row.ja.lower()

        encoded_en = lucy.encode(line_en, return_tensors="pt")[0]
        encoded_ja = lucy.encode(line_ja, return_tensors="pt")[0]

        len_en = len(encoded_en)
        len_ja = len(encoded_ja)

        if len_en <= 1 or len_ja <= 1:
            print(f"Invalid :{line_ja} => {line_en}.\nToo short: {len_ja}/{len_en}")
            return False
        elif len_en > 128 or len_ja > 128:
            print(f"Invalid :{line_ja} => {line_en}.\nToo long: {len_ja}/{len_en}")
            return False
        if len_diff(len_en, len_ja) > 500:
            print(f"Invalid :{line_ja} => {line_en}.\nDifference in length: {len_diff(len_en, len_ja)}")
            return False
        score = jaccard_score(encoded_en, encoded_ja)
        if score > 0.8:
            print(f"Invalid :{line_ja} => {line_en}.\nSimilarity score: {score}")
            return False


def score_func(row, validator: RowValidator, bad_align_detector: BadAlignmentDetector):
    try:
        response = client.post(
            "http://0.0.0.0:8899/sugoi/",
            json={"text": row.ja, "sentence1": row.en},
            params={"score": True},
        )
    except httpx.NetworkError:
        sleep(5)
        return score_func(row, validator, bad_align_detector)
    data = response.json()
    row.sugoi = data["text"]
    row.sem_score = data["score"]["sem_score"]
    bad_align_detector.add(row)
    validator.is_valid(row)  # just check, don't drop bad pairs yet
    return row


def print_score(df):
    low_sem_score_percentage = df[df["sem_score"] < 0.2].shape[0] / df.shape[0] * 100
    print(f"Low semantic score: {low_sem_score_percentage}%")


def score(src, overwrite=False, archive=True, sep="\t"):
    dir_name = src.split("/")[-2]
    # df = pd.read_csv(src, delimiter="\t", header=0, escapechar="`")
    df = pd.read_csv(src, delimiter=sep, header=0)

    df = df.query("en != ja").dropna()
    print(df)

    size = df.shape[0]
    df["sugoi"] = [""] * size
    df["sem_score"] = [0] * size

    bad_align_detector = BadAlignmentDetector()
    row_validator = RowValidator()

    df = df.progress_apply(score_func, axis=1, args=[row_validator, bad_align_detector])

    print(df)

    print_score(df)

    if overwrite:
        dest = src
    else:
        dest = f"dataset/data/corpus/lucy/{slugify(dir_name, separator='_')}.csv".lower()

    df.to_csv(
        dest,
        sep="\t",
        escapechar="`",
        encoding="utf-8",
        index=False,
        quoting=csv.QUOTE_MINIMAL,
    )

    if archive:

        archive_src = f"games/{dir_name}"
        archive_dest = f"games/{dir_name}/{slugify(dir_name, separator='_')}.zip"

        df.to_csv(
            f'{archive_src}/preprocessed.csv',
            sep="\t",
            escapechar="`",
            encoding="utf-8",
            index=False,
            quoting=csv.QUOTE_MINIMAL,
        )

        with zipfile.ZipFile(archive_dest, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(f'{archive_src}/preprocessed.csv', 'preprocessed.csv')
            for raw_src in Path(f'{archive_src}/raw/').rglob('*.*'):
                f.write(raw_src, str(raw_src).replace(f'{archive_src}/', ''))


def fake_score(src):
    dir_name = src.split("/")[-2]
    df = pd.read_csv(src, delimiter="\t", header=0, escapechar="`")

    df = df.query("en != ja").dropna()
    print(df)

    size = df.shape[0]
    df["sem_score"] = [1] * size

    dest = f"dataset/data/corpus/lucy/{slugify(dir_name, separator='_')}.csv".lower()

    df.to_csv(
        dest,
        sep="\t",
        escapechar="`",
        encoding="utf-8",
        index=False,
        quoting=csv.QUOTE_MINIMAL,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str)
    parser.add_argument("--overwrite", default=False, action="store_true")
    parser.add_argument("--fake", default=False, action="store_true")
    parser.add_argument("--sep", default="\t")
    args = parser.parse_args()

    if args.fake:
        fake_score(args.csv)
    else:
        score(args.csv, overwrite=args.overwrite, sep=args.sep)
