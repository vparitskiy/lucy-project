import csv
import json
import os
from pathlib import Path


import datasets


def read_large_file(file_handler):
    for line in file_handler:
        yield line


class LucyDataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "line": datasets.Value('string'),
            }
        )
        return datasets.DatasetInfo(
            description='',
            features=features,
            homepage='',
            license='',
            citation='',
        )

    def _split_generators(self, dl_manager):
        data_dir = Path('/home/vitaliy/projects/lucy_project/spm/dataset/')
        file_list = [
            data_dir / 'ja-en.small.txt',
            #       data_dir / 'en_big.txt',
            data_dir / 'ja-en.txt',
            #        data_dir / 'ja_big.txt',
        ]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "file_list": file_list,
                    "split": "train",
                },
            ),
            # datasets.SplitGenerator(
            #     name=datasets.Split.TEST,
            #     # These kwargs will be passed to _generate_examples
            #     gen_kwargs={
            #         "en": os.path.join(data_dir, "dataset.en"),
            #         "ja": os.path.join(data_dir, "dataset.ja"),
            #         "split": "train",
            #     },
            # ),
            # datasets.SplitGenerator(
            #     name=datasets.Split.VALIDATION,
            #     # These kwargs will be passed to _generate_examples
            #     gen_kwargs={
            #         "en": os.path.join(data_dir, "dataset.en"),
            #         "ja": os.path.join(data_dir, "dataset.ja"),
            #         "split": "train",
            #     },
            # ),
        ]

    def _generate_examples(self, file_list, split):
        idx = 0
        for src in file_list:
            with open(src) as f:
                # Create a generator object for the file: gen_file
                for line in read_large_file(f):
                    yield idx, {'line': line.strip()}
                    idx += 1
