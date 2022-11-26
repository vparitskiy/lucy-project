from typing import Union

import datasets
import pandas as pd
from datasets import Dataset, DatasetDict


def df2dataset(df: pd.DataFrame) -> datasets.DatasetDict:
    train = datasets.Dataset.from_pandas(df)
    train = datasets.Dataset.from_dict({"translation": train})
    dataset = datasets.DatasetDict({"train": train})
    return dataset


def split_dataset(dataset: Union[Dataset, DatasetDict], test_size=0.1):
    if isinstance(dataset, DatasetDict):
        dataset = dataset["train"]
    train_test_valid = dataset.train_test_split(shuffle=True, test_size=test_size)
    test_valid = train_test_valid["test"].train_test_split(test_size=0.5)

    return DatasetDict(
        {
            "train": train_test_valid["train"],
            "test": test_valid["test"],
            "validation": test_valid["train"],
        }
    )
