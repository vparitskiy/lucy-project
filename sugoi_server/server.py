import logging
from pathlib import Path

import ctranslate2
import sentencepiece as spm
import torch
import uvicorn
from fairseq.models.transformer import TransformerModel
from sentence_transformers import SentenceTransformer, util
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from transformers import MT5Tokenizer
from transformers import set_seed

logger = logging.getLogger()

logger.setLevel("DEBUG")
logger = logging.getLogger("uvicorn.error")


# SUGOI_VER = 'sugoi_3.3'
SUGOI_VER = 'sugoi_4.4'


def get_sugoi_pipeline(root):
    set_seed(42)
    ja2en = TransformerModel.from_pretrained(
        f"{root}/{SUGOI_VER}",
        checkpoint_file="big.pretrain.pt",
        source_lang="ja",
        target_lang="en",
        bpe="sentencepiece",
        sentencepiece_model=f"{root}/{SUGOI_VER}/spm.ja.nopretok.model",
        is_gpu=True,
        no_repeat_ngram_size=3,
    )
    ja2en.cuda()
    return ja2en.translate


def get_sugoi_ct2_pipeline(root):
    target_spm = spm.SentencePieceProcessor(f"{root}/{SUGOI_VER}/spm.en.nopretok.model")
    source_spm = spm.SentencePieceProcessor(f"{root}/{SUGOI_VER}/spm.ja.nopretok.model")

    translator = ctranslate2.Translator(model_path=f"{root}/{SUGOI_VER}_ct2/", device="cuda")

    def translate(s):
        line = source_spm.encode(s, out_type=str)
        results = translator.translate_batch(
            [line],
            beam_size=2,
            no_repeat_ngram_size=3,
            normalize_scores=True,
            allow_early_exit=True,
        )
        return target_spm.decode(results[0].hypotheses)[0]

    return translate


class Pipeline:
    models_root = Path(__file__).parent.parent / "models"
    sugoi = None
    gtrans = None
    score_model = None
    score_tokenizer = None

    def init(self):
        self.sugoi = get_sugoi_ct2_pipeline(self.models_root)
        # self.sugoi = get_sugoi_pipeline(self.models_root)
        self.score_model = SentenceTransformer(f"{self.models_root}/all-MiniLM-L12-v2")
        self.score_tokenizer = MT5Tokenizer.from_pretrained(f"{self.models_root}/satou")

    def translate(self, sentence: str) -> str:
        return self.sugoi(sentence).replace("<unk>", "")

    def score(self, sentence1, sentence2) -> dict:
        return {
            "sem_score": self.sem_score(sentence1, sentence2),
        }

    def sem_score(self, sentence1, sentence2) -> float:
        embeddings1 = self.score_model.encode(sentence1.lower(), convert_to_tensor=True)
        embeddings2 = self.score_model.encode(sentence2.lower(), convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
        return torch.diag(cosine_scores).cpu().numpy()[0].astype(float)


pipeline = Pipeline()


async def handle_sugoi(request):
    data = await request.json()
    result = {"text": pipeline.translate(data["text"])}
    if request.query_params.get("score"):
        result["score"] = pipeline.score(data["sentence1"], result["text"])
    return JSONResponse(result)


async def handle_score(request):
    data = await request.json()
    result = pipeline.score(data["sentence1"], data["sentence2"])
    response = JSONResponse(result)
    return response


routes = [
    Route("/sugoi/", endpoint=handle_sugoi, methods=["POST"]),
    Route("/score/", endpoint=handle_score, methods=["POST"]),
]

app = Starlette(
    debug=False,
    routes=routes,
    on_startup=[pipeline.init],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8899)
