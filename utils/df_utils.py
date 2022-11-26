import csv
from typing import Callable

import mapply
import numpy as np
import pandas as pd

from utils.normalize_text import normalize_en, normalize_ja

mapply.init()


def save_dataframe(
    df: pd.DataFrame,
    pre_process_ja: Callable[[str], str] = None,
    pre_process_en: Callable[[str], str] = None,
    post_process_en: Callable[[str], str] = None,
    post_process_ja: Callable[[str], str] = None,
    file_name: str = None,
    trans_full=True,
):
    def _process_ja(str_ja):
        str_ja = str(str_ja)
        if pre_process_ja:
            str_ja = pre_process_ja(str_ja)
        str_ja = normalize_ja(str_ja, trans_full=trans_full)
        if post_process_ja:
            str_ja = post_process_ja(str_ja)
        return str_ja or np.nan

    def _process_en(str_en):
        str_en = str(str_en)
        if pre_process_en:
            str_en = pre_process_en(str_en)
        str_en = normalize_en(str_en)
        if post_process_en:
            str_en = post_process_en(str_en)
        return str_en or np.nan

    df = df.drop_duplicates().query("en != ja")

    print(df)

    df["en"] = df.en.mapply(_process_en)
    df["ja"] = df.ja.mapply(_process_ja)

    df = df.dropna()

    df["en"] = df["en"].astype("string")
    df["ja"] = df["ja"].astype("string")

    df = df.drop_duplicates().query("en != ja")
    print(df)
    df.to_csv(
        file_name or "dataset.csv",
        sep="\t",
        encoding="utf-8",
        index=False,
        escapechar="`",
        quoting=csv.QUOTE_MINIMAL,
    )
