import re


def iter_lines(lines, sep="-----", join=" "):
    sent = ""
    for line in lines:
        if line.startswith(sep):
            if sent:
                yield sent
            sent = ""
            continue
        sent += join + line
    if sent:
        yield sent


cp932 = "cp932"
shift_jis = "shift-jis"
cp1252 = "cp1252"
utf_16le = "utf-16le"


def ruby_strip(s):
    "<ruby=よくぼう>夢</ruby>"
    s = re.sub(r"<ruby=.*?>", "", s)
    s = re.sub(r"</ruby>", "", s)
    assert s
    return s
