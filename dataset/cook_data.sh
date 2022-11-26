#./scripts/get_public_data.sh -c wikimatrix
#./scripts/get_public_data.sh -c paracrawl
#python scripts/extract_wikimatrix.py --threshold=1.05 --src-lang=en --trg-lang=ja --tsv=data/corpus/wikimatrix/WikiMatrix.v1.en-ja.langid.tsv --bitext=data/train/raw/wikimatrix
#python scripts/extract_paracrawl.py --txt data/corpus/paracrawl/en-ja/en-ja.bicleaner05.txt --bitext data/train/raw/paracrawl --threshold=0.77
#python scripts/extract_anime_subtitles.py --semantic_score=0.2 --src-lang=ja --trg-lang=en --csv=data/corpus/clean_anime_subtitles.csv --bitext=data/train/raw/anime_subtitles
#python scripts/extract_lucy.py
#scripts/clean_lucy.sh -c 1
#scripts/clean_en.sh -c anime_subtitles -c jarunc -c paracrawl -c wikimatrix -c ted
#scripts/clean_ja.sh -c anime_subtitles -c jarunc -c paracrawl -c wikimatrix -c ted
#python scripts/preprocess.py --input=anime_subtitles
#python scripts/preprocess.py --input=wikimatrix
#python scripts/preprocess.py --input=paracrawl
#python scripts/preprocess.py --input=jarunc
#scripts/concatenate_bitext.sh -c train/raw