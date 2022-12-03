from tokenizers.models import Unigram
from datasets import load_dataset
from tokenizers import Regex, Tokenizer, decoders, normalizers, pre_tokenizers, trainers
from tokenizers.models import Unigram
from tokenizers.processors import TemplateProcessing
from tokenizers.tokenizers import AddedToken

# for i in range(256):
#     token = f"<0x{i:02x}>".upper()
#     print('added_token: ', token)
#     special_tokens.append(AddedToken(token, special=False))

replacement = "▁"
unk_id = 2

tokenizer = Tokenizer(Unigram())
tokenizer.add_special_tokens(
    [
        AddedToken('<pad>'),
        AddedToken('</s>'),
        AddedToken('<unk>'),
    ]
)
tokenizer.normalizer = normalizers.Sequence(
    [
        normalizers.Nmt(),
        normalizers.NFKC(),
        normalizers.Replace(Regex(" {2,}"), " "),
    ]
)
tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
    [
        pre_tokenizers.UnicodeScripts(),
        pre_tokenizers.Digits(individual_digits=True),
        pre_tokenizers.Metaspace(replacement=replacement, add_prefix_space=True),
    ]
)

tokenizer.decoder = decoders.Metaspace(
    replacement=replacement,
    add_prefix_space=True,
)


tokenizer.post_processor = TemplateProcessing(
    single="$A </s>",
    pair="$A </s> $B </s>",
    special_tokens=[("</s>", 1)],
)

raw_dataset = load_dataset("./dataset/load.py", streaming=True)


def get_training_corpus():
    dataset = raw_dataset["train"]
    for i in dataset:
        yield i['line']


training_corpus = get_training_corpus()

trainer = trainers.UnigramTrainer(unk_token='<unk>', vocab_size=65536, special_tokens=["<pad>", "</s>", "<unk>"])

tokenizer.train_from_iterator(training_corpus, trainer=trainer)

tokenizer.save("lucy-toc-65536/tokenizer.json")
