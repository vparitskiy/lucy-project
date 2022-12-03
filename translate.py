import argparse

from transformers import (
    MT5ForConditionalGeneration,
    MT5Tokenizer,
    Text2TextGenerationPipeline,
)
from transformers import set_seed

from utils.normalize_text import normalize_ja

set_seed(42)


def create_pipeline():
    model_config = dict(pretrained_model_name_or_path="train/lucy-base/checkpoint-2511")

    tokenizer = MT5Tokenizer.from_pretrained(**model_config)

    pipeline = Text2TextGenerationPipeline(
        model=MT5ForConditionalGeneration.from_pretrained(**model_config),
        tokenizer=tokenizer,
        device="cpu",
    )

    vocab = tokenizer.get_vocab()
    pipeline.vocab = vocab
    return pipeline


pipeline = create_pipeline()


def translate(sentence):

    sentence = normalize_ja(sentence)

    tokenizer = pipeline.tokenizer
    vocab = pipeline.vocab
    tok = tokenizer.tokenize(sentence)
    print(tok, [t in vocab for t in tok])
    # sentences, endls = split_sentences(sentence)

    # input_src = prepare_simple(sentences, src_lang, trg_lang)
    # input_src = text_utils.prepare_contexts(sentences, src_lang, trg_lang)

    print(sentence)

    config = dict(
        num_beams=4,
        do_sample=True,
        temperature=1.0,
        batch_size=8,
        max_length=128,
        no_repeat_ngram_size=4,
        repetition_penalty=1.2,
        early_stopping=True,
    )

    outputs = pipeline(sentence, **config)
    print(outputs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("s", type=str, default="s")
    parser.add_argument("--checkpoint", type=int)

    args = parser.parse_args()

    translate(args.s)
