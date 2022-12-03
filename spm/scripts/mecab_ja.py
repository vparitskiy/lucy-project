import MeCab

mecab = MeCab.Tagger("-Owakati")
with open('ja.txt') as fin:
    with open('ja-tok.txt', 'w') as fout:
        for line in fin.read().split('\n'):
            fout.write(mecab.parse(line))
