import os.path
import re
from itertools import zip_longest
from pathlib import Path

import pandas as pd

re_og = re.compile(r"^    \w+\s\".*?\"|^    \".*?\"", re.MULTILINE)
re_tl = re.compile(r"^    \w+\s\".*\"|^    \".*?\"", re.MULTILINE)


def get_og_strings(data: str):
    return [clean_tags(s.strip()) for s in re.findall(re_og, data)]


def get_tl_strings(data: str):
    return [clean_tags(s.strip()) for s in re.findall(re_tl, data)]


def clean_tags(s):
    s = re.sub(r"(\{rt\}.*?\{/rt\})+", "", s)
    for block in re.findall(r"\{rb\}.*?\{/rb\}", s):
        sub = block.replace("{rb}", "").replace("{/rb}", "")
        s = s.replace(block, sub)
    return s


def clean_quotes(s):
    if s.startswith('"') or s.startswith("\\"):
        while s.startswith('"') or s.startswith("\\"):
            s = s[1:]
    if s.endswith('"') or s.endswith("\\"):
        while s.endswith('"') or s.endswith("\\"):
            s = s[:-1]
    return s


def parse(og_scenario_src: Path, tl_scenario_src: Path, chara_map: dict, tl_files=()):
    for og_src in og_scenario_src.rglob("*.rpy"):

        with open(og_src) as f:
            og_data = f.read()

        og_strings = get_og_strings(og_data)
        og_fixed = []
        for s in og_strings:
            s = clean_quotes(s)
            for key in chara_map.keys():
                if s.startswith(f"{key} "):
                    s = s.replace(f"{key} ", "").strip()
                    s = clean_quotes(s)
                    s = f'{chara_map[key]["og"]} {s}'
            og_fixed.append(s)

        with open(tl_scenario_src / os.path.basename(og_src)) as f:
            tl_data = f.read()

        tl_strings = get_tl_strings(tl_data)
        tl_fixed = []
        for s in tl_strings:
            quotes = True
            for key in chara_map.keys():
                if s.startswith(f"{key} "):
                    quotes = False
                    s = s.replace(f"{key} ", "").strip()
                    s = clean_quotes(s)
                    s = f'{chara_map[key]["tl"]}: "{s}"'
            if quotes:
                s = clean_quotes(s)
            tl_fixed.append(s)

        og_list = []
        tl_list = []
        for og, tl in zip_longest(og_fixed, tl_fixed):
            og_list.append(og)
            tl_list.append(tl)
        df = pd.DataFrame.from_dict({"og": og_list, "tl": tl_list})
        df.to_csv(f"raw/csv/{os.path.basename(og_src)}.csv", sep="\t", escapechar="`")

        og_list = []
        tl_list = []

        for src in tl_files:
            with open(src) as f:
                data = f.read()
            for line in re.findall(re_og, data):
                line = line.strip()
                if line.startswith("old "):
                    line = line.replace("old ", "").strip()
                    line = clean_quotes(line)
                    og_list.append(line)
                if line.startswith("new "):
                    line = line.replace("new ", "").strip()
                    line = clean_quotes(line)
                    tl_list.append(line)
        df = pd.DataFrame.from_dict({"og": og_list, "tl": tl_list})
        df.to_csv(f"raw/csv/tl_files.csv", sep="\t", escapechar="`")
