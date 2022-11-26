import re

from luaparser import ast
from luaparser import astnodes


def clean(s):
    # @@@@{@@@@@"恵麻の舌が私の口の中に入ってくる。",@@@@@{"rt2"},@
    s = s.replace("@", "")
    s = re.sub(r'\{"ruby", text=".*?"\}', "", s)
    s = re.sub(r'\{"/ruby"\},', "", s)

    loc_name = bool(re.search(r'name = \{".*?", ".*?"\}', s))

    strings = re.findall('"(.*?)"', s)
    if loc_name:
        s = f'{strings[1]}: "{"".join(strings[2:])}"'
        s = s.replace('" (', "(").replace(') "', ")")
    else:
        s = " ".join(strings)
    s = s.replace("rt2", "")
    return s


def parse_multilang(src):

    with open(src) as f:
        data = f.read()

    ja_data = []
    en_data = []
    tree = ast.parse(data)
    for node in ast.walk(tree):
        if isinstance(node, astnodes.Field):
            if isinstance(node.key, astnodes.Name):
                if node.key.id == "ja":
                    table = node.value
                    ja_data.append(
                        [
                            st.s
                            for st in ast.walk(table)
                            if isinstance(st, astnodes.String) and st.s not in ["rt2"]
                        ]
                    )
                if node.key.id == "en":
                    table = node.value
                    en_data.append(
                        [
                            st.s
                            for st in ast.walk(table)
                            if isinstance(st, astnodes.String) and st.s not in ["rt2"]
                        ]
                    )
    ja_data = [
        " ".join([s.replace("\\", " ") for s in sent if s and s not in ["name"]])
        for sent in ja_data
        if sent
    ]
    en_data = [
        " ".join([s.replace("\\", " ") for s in sent if s and s not in ["name"]])
        for sent in en_data
        if sent
    ]
    print(f"ja: {len(ja_data)} en: {len(en_data)}")
    assert len(ja_data) == len(en_data)
    return ja_data, en_data


tags = ["ka_", "vo  ", "ao_", "name", "si_"]
tags_exact = {
    "vo",
    "name",
    "text",
    "bg",
    "se",
    "ex",
    "select",
    "cgdel",
    "bgm",
    "extrans",
    "vostop",
    "colortone",
    "timezone",
    "sceneend",
    "excall",
    "eval",
    "fg",
    "quake",
    "exfont",
    "rt2",
    "fgact",
    "mwf",
    "love",
    "eval",
    "zapping",
    "rtc",
    "exreturn",
    "ruby",
    "/ruby",
    "msgoff",
    "chselect",
    "steamacv",
    "vol",
}


def parse_monolang(src):

    with open(src) as f:
        data = f.read()

    lang_data = []
    tree = ast.parse(data)

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Field)
            and isinstance(node.key, astnodes.Number)
            and isinstance(node.value, astnodes.String)
            and node.key.n == 1
        ):
            string = node.value.s.strip().replace("\n", " ")
            if string in tags_exact:
                continue
            lang_data.append(string)
    print(f"{len(lang_data)}")
    return lang_data


def clean_v1(s):
    # @@@@{@@@@@"恵麻の舌が私の口の中に入ってくる。",@@@@@{"rt2"},@
    s = s.replace("@", "").strip().replace('"\\', "").replace("\\", "")
    s = re.sub('name=".*?"', "", s)
    strings = re.findall('"(.*?)"', s)

    # loc_name = bool(re.search(r'name = \{".*?", ".*?"\}', s))
    #
    # strings = re.findall('"(.*?)"', s)
    # if loc_name:
    #     s = f'{strings[1]}: "{"".join(strings[2:])}"'
    #     s = s.replace('" (', "(").replace(') "', ")")
    # else:
    s = " ".join(strings)
    s = s.replace("rt2", "")
    return s


def parse_v1(data):
    ja_data = []
    en_data = []
    data = (
        data.replace("\n", "").replace("{", "@").replace("},", "@").replace("},", "@")
    )
    for ja in re.findall(r"@ja=@(.*?)@@en", data):
        ja_data.append(clean_v1(ja))
    for en in re.findall(r"@en=@(.*?)@@tw", data):
        en_data.append(clean_v1(en))

    return en_data, ja_data
