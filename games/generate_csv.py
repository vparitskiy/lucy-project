import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
import os.path
import re
import json


import pandas as pd


from utils.unicode import range_ja
from utils.df_utils import save_dataframe


def pre_common(s: str) -> str:
    return s


def pre_en_row(s: str) -> str:
    s = pre_common(s)
    if re.findall(r'[{}]'.format(range_ja), s):
        return ''
    return s


def post_en_row(s: str) -> str:
    return s


def pre_ja_row(s: str) -> str:
    s = pre_common(s)
    if not re.findall(r'[{}]'.format(range_ja), s):
        return ''
    return s


def post_ja_row(s: str) -> str:
    return s


def main():
    csv_data = {"ja": [], "en": []}

    root = Path(__file__).parent / "raw"

    df = pd.DataFrame.from_dict(csv_data)
    save_dataframe(
        df,
        pre_process_en=pre_en_row,
        post_process_en=post_en_row,
        pre_process_ja=pre_ja_row,
        post_process_ja=post_ja_row,
        trans_full=False,
    )


if __name__ == "__main__":
    main()
