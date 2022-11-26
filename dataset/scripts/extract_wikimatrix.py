#!/bin/python3
# Modified from the original script at: https://github.com/facebookresearch/LASER/blob/master/tasks/WikiMatrix/extract.py
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# LASER  Language-Agnostic SEntence Representations
# is a toolkit to calculate multilingual sentence embeddings
# and to use them for document classification, bitext filtering
# and mining
#
# --------------------------------------------------------
#
# Tool to extract subset of mined bitexts in a tsv file

import argparse

###############################################################################
#
# Main
#
###############################################################################


parser = argparse.ArgumentParser(
    description="Tool to extract bitext from the WikiMatrix"
)
parser.add_argument(
    "--encoding", default="utf-8", help="character encoding for input/output"
)
parser.add_argument("--tsv", type=str, required=True, help="File with mined bitexts")
parser.add_argument(
    "--bitext", type=str, required=True, help="Text file after sentence splitting"
)
parser.add_argument("--src-lang", type=str, required=True, help="Source language")
parser.add_argument("--trg-lang", type=str, required=True, help="Traget language")
parser.add_argument(
    "--threshold", type=float, default=0.0, help="Threshold on margin score"
)
parser.add_argument(
    "--nb_sents", type=int, default=999999999, help="Maximal number of sentences"
)
parser.add_argument(
    "--nb-words-src",
    type=int,
    default=999999999,
    help="Maxmimal numer of total words in the source language",
)
parser.add_argument(
    "--nb-words-trg",
    type=int,
    default=999999999,
    help="Maxmimal numer of total words in the target language",
)
args = parser.parse_args()

print("Tool to extract bitext from the WikiMatrix")

nl = 0
nw_src = 0
nw_trg = 0
print("Processing {}".format(args.tsv))
with open(args.tsv, "rt", encoding=args.encoding) as tsv:
    with open(args.bitext + "." + args.src_lang, "wt", encoding=args.encoding) as fsrc:
        with open(
            args.bitext + "." + args.trg_lang, "wt", encoding=args.encoding
        ) as ftrg:
            while nl < args.nb_sents:
                line = tsv.readline()
                if not line:
                    break
                fields = line.split("\t")
                cur_src = len(fields[1].split())
                cur_trg = len(fields[2].split())
                if float(fields[0]) < args.threshold:
                    break
                if nw_src + cur_src > args.nb_words_src:
                    break
                if nw_trg + cur_trg > args.nb_words_trg:
                    break
                # Modified from the original script to filter out sentences with the wrong lang id.
                if fields[3].strip() != args.src_lang:
                    continue
                if fields[4].strip() != args.trg_lang:
                    continue
                fsrc.write(fields[1].strip() + "\n")
                ftrg.write(fields[2].strip() + "\n")
                nw_src += cur_src
                nw_trg += cur_trg
                nl += 1
                if nl % 100000 == 0:
                    print("\r - {:d} lines read".format(nl), end="")

print("\r - wrote {:d} lines".format(nl))
print(" - with {:d} source and {:d} target words".format(nw_src, nw_trg))
print(" - last threshold is {:.4f}".format(float(fields[0])))
