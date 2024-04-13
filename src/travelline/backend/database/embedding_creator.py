#!/usr/bin/env python3

"""
@author - Zaitsev Vasilii, 2024

"""

import os
import sys

sys.path.append("../rag")

from sbertembedding import SBertEmbedding
from pathlib import Path
import os
import torch


DOCS_TXT_DIR = "../../docs_txt"
EMBEDDING_DIR = "./embeddings"


def crop_filename(filename):
    return filename.split("/")[-1].split("#")[-2]


def main() -> None:
    embedding = SBertEmbedding()

    in_dir_path = Path(DOCS_TXT_DIR).absolute()
    out_dir_path = Path(EMBEDDING_DIR).absolute()

    if not in_dir_path.exists():
        print(f"{in_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    if not out_dir_path.exists():
        print(f"{out_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    for filename in os.listdir(in_dir_path.as_posix()):
        filename = os.path.join(in_dir_path.as_posix(), filename)

        with open(filename, "r", encoding="utf-8") as file:
            doc_data = file.read()
        q = torch.nn.functional.normalize(embedding.get(doc_data))

        print(f"Created embedding {out_dir_path}/{crop_filename(filename)}.pt")
        torch.save(q, f"{out_dir_path}/{crop_filename(filename)}.pt")

    print("Embedding dumping finished!")


if __name__ == "__main__":
    main()
