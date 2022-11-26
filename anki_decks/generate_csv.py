import os
import re
import sys
from pathlib import Path
from slugify import slugify
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from utils.df_utils import save_dataframe


def normalize_en_row(s):
    s = re.sub("（.*?）", "", s)
    s = re.sub("\(.*?\)", "", s)
    return s


def normalize_ja_row(s):
    s = re.sub("（.*?）", "", s)
    s = re.sub("\(.*?\)", "", s)
    return s


def main():
    for path in (Path(__file__).parent / "csv").rglob("Attack on Titan Season 4 - Part 2 (Eng + Jp).apkg.csv"):

        csv_data = {"ja": [], "en": []}

        df: pd.DataFrame = pd.read_csv(path, sep=",", header=None, encoding="utf-8").iloc[:, [6]]

        for row in df.itertuples():
            row = row._1

            row = re.sub(r"+", "", row)
            parts = row.split("")

            if len(parts) == 1:
                continue

            text_ja = parts[1].strip()
            text_en = parts[2].strip()

            if text_en.startswith('...') or text_en.endswith('...'):
                continue

            text_ja = text_ja.replace('➡', '')
            if '♬' in text_ja:
                continue

            csv_data["ja"].append(text_ja)
            csv_data["en"].append(text_en)

        df = pd.DataFrame.from_dict(csv_data)
        file_name = str(path).split("/")[-1].split(".")[0]
        dest = f"datasets/{slugify(file_name, separator='_')}"
        os.makedirs(dest, exist_ok=True)
        save_dataframe(
            df,
            pre_process_ja=normalize_ja_row,
            pre_process_en=normalize_en_row,
            file_name=f"{dest}/dataset.csv",
        )


if __name__ == "__main__":
    main()
