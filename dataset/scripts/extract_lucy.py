import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent.parent))


tqdm.pandas()

root = Path(__file__).parent.parent

df = pd.concat(
    [
        pd.read_csv(src, delimiter="\t", escapechar="`", quoting=csv.QUOTE_MINIMAL, header=0)
        for src in (root / "data" / "corpus" / "lucy").rglob("*.csv")
    ],
    ignore_index=True,
)

df = df.query("sem_score>0.2").drop_duplicates().query("en != ja").query("en != ''").query("ja != ''")

print(df)

np.savetxt(root / "data" / "raw" / "lucy.en", df["en"].values, fmt="%s")
np.savetxt(root / "data" / "raw" / "lucy.ja", df["ja"].values, fmt="%s")
