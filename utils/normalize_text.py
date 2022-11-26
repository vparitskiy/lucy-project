import argparse
import html
import re
import unicodedata

import lxml.html
import lxml.html.clean
from lxml.etree import ParserError
from sudachipy import dictionary
from sudachipy import tokenizer


def clean_html(s):
    if not s:
        return ""
    try:
        doc = lxml.html.fromstring(s)
    except ParserError:
        return s
    cleaner = lxml.html.clean.Cleaner(style=True)
    doc = cleaner.clean_html(doc)
    return doc.text_content()


def unicode_normalize(cls, s):
    pt = re.compile("([{}]+)".format(cls))

    def norm(c):
        return unicodedata.normalize("NFKC", c) if pt.match(c) else c

    s = "".join(norm(x) for x in re.split(pt, s))
    return s


def maketrans(f, t):
    return {ord(x): ord(y) for x, y in zip(f, t)}


re_non_print = re.compile(
    r"[\uFEFF\u200B\u2003\u2060\u2009\u0000-\u0008\u000B-\u001F\u007F-\u009F\u2000-\u200F\u2028-\u202F\u205F-\u206F\u3000]+"
)

re_whitespace = re.compile(r"[\u000A\u000B\u000C\u000D\u0085\u2028\u2029\u00A0\u2003\u3000\u0009]+")

re_null_byte = re.compile("[\x00\x08\x0B\x0C\xa0\x0E-\x1F]+")


def __clean_common(s):
    s = s.replace("\u005C\u0072\u005C\u006E", " ")  # \r\n
    s = s.replace("\u005C\u006E", " ")  # \n
    s = s.replace("\u005C\u0074", " ")  # \t

    s = html.unescape(s)
    s = clean_html(s)
    s = re.sub("[ 　]+", " ", s)
    s = re.sub(re_null_byte, "", s)
    s = re.sub(re_non_print, "", s)
    s = re.sub(re_whitespace, " ", s)

    s = unicode_normalize("０-９Ａ-Ｚａ-ｚ｡-ﾟ", s)
    s = re.sub("[˗֊‐‑‒–⁃⁻-₋−]+", "–", s)  # normalize dashes
    s = re.sub("[﹣－ｰ―─━ー—]+", "—", s)  # normalize colons
    s = re.sub("[〜∼∾〰～]+", "~", s)  # normalize tildes

    return s


def __remove_extra_spaces(s: str) -> str:
    s = re.sub("[ 　]+", " ", s)
    blocks = "".join(
        (
            "\u4E00-\u9FFF",  # CJK UNIFIED IDEOGRAPHS
            "\u3040-\u309F",  # HIRAGANA
            "\u30A0-\u30FF",  # KATAKANA
            "\u3000-\u303F",  # CJK SYMBOLS AND PUNCTUATION
            "\uFF00-\uFFEF",  # HALFWIDTH AND FULLWIDTH FORMS
        )
    )
    basic_latin = "\u0000-\u007F"

    def remove_space_between(cls1: str, cls2: str, s: str) -> str:
        p = re.compile("([{}]) ([{}])".format(cls1, cls2))
        while p.search(s):
            s = p.sub(r"\1\2", s)
        return s

    s = remove_space_between(blocks, blocks, s)
    s = remove_space_between(blocks, basic_latin, s)
    s = remove_space_between(basic_latin, blocks, s)
    return s


def normalize_en(s):
    s = str(s)
    s = s.strip()
    if s.isdigit():
        return ""
    s = __clean_common(s)
    s = s.translate(
        maketrans(
            "！”＃＄％＆’（）＊＋，､－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。｡、・「」『』【】《》“”",
            '!"#$%&\'()*+,,-./:;<=>?@[¥]^_`{|}~..,-""""""""""',
        )
    )
    s = unicode_normalize("!\"#$%&'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣『』", s)
    # if len(s.split()) > 2 and s.isupper():
    #     s = s.capitalize()
    return s


sudachipy_tokenizer = dictionary.Dictionary().create()
re_katakana = re.compile(r"[\u30A0-\u30FF\u31F0-\u31FF]")


def normalize_katakana(line):
    mode = tokenizer.Tokenizer.SplitMode.A
    tokens = [m for m in sudachipy_tokenizer.tokenize(line, mode)]
    new_tokens = []
    for token in tokens:
        if "名詞" in token.part_of_speech() and re.match(re_katakana, str(token)):
            new_tokens.append(token.normalized_form())
        else:
            new_tokens.append(token.surface())
    new_line = "".join(new_tokens)
    return new_line


def normalize_ja(s, trans_full=False):
    s = str(s)
    s = s.strip()
    if s.isdigit():
        return ""
    s = __clean_common(s)

    if trans_full:
        trans = maketrans(
            "!\"#$%&'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣",
            "！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」",
        )
    else:
        trans = maketrans(".`~｡､･｢｣", "．｀〜。、・「」")

    s = s.translate(trans)
    s = normalize_katakana(s)
    s = __remove_extra_spaces(s)
    return normalize_katakana(s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str)

    args = parser.parse_args()
    print(normalize_ja(args.s))
