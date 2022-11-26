import json


def clean_tags(s):
    if s.startswith("≪") and s.endswith("≫"):
        s = s[1:-1]
    if s.startswith("<<") and s.endswith(">>"):
        s = s[2:-2]
    return s


def get_text(array):
    for i in array[::-1]:
        if isinstance(i, str):
            return i


def parse(src, text_index=2):

    with open(src) as f:
        data = json.load(f)

    scenes = data["scenes"]
    for scene in scenes:
        texts = scene.get("texts", [])
        for text in texts:
            if not text[text_index]:
                continue
            col_ja = text[text_index][0]
            try:
                col_en = text[text_index][1]
            except IndexError:
                continue
            ja = get_text(col_ja)
            en = get_text(col_en)
            yield clean_tags(ja), clean_tags(en)
