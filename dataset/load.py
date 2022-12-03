import csv
import json
import os
from pathlib import Path


import datasets


class LucyDataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value('string'),
                "translation": datasets.features.Translation(languages=['ja', 'en']),
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
        data_dir = Path('/home/vitaliy/projects/lucy_project/dataset/data/')
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "en": data_dir / "train" / "dataset.en",
                    "ja": data_dir / "train" / "dataset.ja",
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

    def _generate_examples(self, en, ja, split):
        with open(en, encoding="utf-8") as f_en:
            with open(ja, encoding="utf-8") as f_ja:
                for idx, row in enumerate(zip(f_ja.readlines(), f_en.readlines())):
                    yield idx, {
                        "id": idx,
                        "translation": {
                            "ja": row[0].strip(),
                            "en": row[1].strip(),
                        },
                    }
