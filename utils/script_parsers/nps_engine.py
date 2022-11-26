import re


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


re_box = re.compile(r'<box type="9">(.*?)<box type="0">', flags=re.DOTALL)


def parse(data):
    sents = []
    res = []
    sent = ""

    for block in re.findall(re_box, data):
        for idx, line in enumerate(block.splitlines()):
            if line.startswith(" ") or line.startswith("　") or idx == 0:
                if sent:
                    sents.append(sent)
                sent = ""
            sent = sent + " " + line

        for s in sents:
            s = s.replace("//", "").strip()
            s = re.sub("<.*?>", "", s)
            if s:
                res.append(s)
        sents = []
        # for segment in re.split("<k>|\n\n", block):
        #     for m in re.findall(r'<R TEXT=".*?">.*<\/R>', segment):
        #         s = re.sub("<.*?>", "", m)
        #         segment = segment.replace(m, s)
        #     segment = re.sub("<.*?>", "", segment)
        #     res.append(segment.replace("\n", " ").strip())
    return res
