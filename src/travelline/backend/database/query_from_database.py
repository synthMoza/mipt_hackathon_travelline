#!/usr/bin/env python3

"""
@author - Zaitsev Vasilii, 2024

"""

import os
import sys

import numpy as np
import torch
import argparse
from sklearn.metrics.pairwise import cosine_similarity
from travelline.backend.rag.sbertembedding import SBertEmbedding
from pathlib import Path
from typing import List, Tuple, Dict


repo_root = Path(__file__).parent.parent.parent.parent.parent

EMBEDDING_DIR = repo_root / "src" / "travelline" / "backend" / "database" / "embeddings"
NUMBER_OF_SIMILAR_FILES = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Returns most similar file to the passed query")
    parser.add_argument("-q", "--query", type=str, help="Query to database", required=True)
    return parser.parse_args(sys.argv[1:])


def load_tensors(embedding_dir: str) -> Tuple[List[torch.Tensor], Dict[int, str]]:
    list_tensor = []
    dict_with_indexes = {}
    emb_dir_path = Path(embedding_dir).absolute()

    if not emb_dir_path.exists():
        print(f"{emb_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    index = 0
    for filename_short in os.listdir(emb_dir_path.as_posix()):
        filename = os.path.join(emb_dir_path.as_posix(), filename_short)
        list_tensor.append(torch.load(filename, weights_only=True))
        dict_with_indexes[index] = filename_short.split(".pt")[0]
        index += 1

    return (list_tensor, dict_with_indexes)


def embed_query(query: str) -> torch.Tensor:
    embedding = SBertEmbedding()
    return embedding.get(query)


def main() -> None:
    # args = parse_args()
    (tensor_list, dict_with_indexes) = load_tensors(EMBEDDING_DIR)
    tensors = np.vstack(tensor_list)

    print("Database loaded")

    while True:
        print("")
        print("*******************")
        print("Please input your query")
        # user_query = args.query
        user_query = input()

        # start_time = time.time()
        emb_query = torch.nn.functional.normalize(embed_query(user_query))
        # print(f"Time: {time.time() - start_time}")
        # print(f"User query: {user_query}")
        query_similarities = cosine_similarity([emb_query[0]], tensors)[0]

        # most_similar_index = np.argmax(query_similarities)
        similarity_list = []
        for index in range(len(dict_with_indexes)):
            similarity_list.append((dict_with_indexes[index], query_similarities[index]))

        similarity_list.sort(key=lambda x: x[1], reverse=True)
        print(f"Similarity list = {similarity_list}")
        tmp_num = NUMBER_OF_SIMILAR_FILES
        print(f"Top {tmp_num} similar files: {[x[0] for x in similarity_list[:tmp_num]]}")
        print("********************")


if __name__ == "__main__":
    main()
