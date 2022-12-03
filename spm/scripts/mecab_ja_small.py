import MeCab

mecab = MeCab.Tagger("-Owakati")
with open('dataset/ja_small_1.txt') as fin:
    with open('ja_small.txt', 'w') as fout:
        for line in fin.read().split('\n'):
            fout.write(mecab.parse(line))
