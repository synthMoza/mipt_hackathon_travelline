#!/usr/bin/env python3

import os
import sys

sys.path.append("../rag")

import numpy as np
import torch
import argparse
from sklearn.metrics.pairwise import cosine_similarity
from sbertembedding import SBertEmbedding
from pathlib import Path
from typing import List, Tuple, Dict

EMBEDDING_DIR = "embeddings"
QUERY = "Как поставить цены в тарифе"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Returns most similar file to the passed query')
    parser.add_argument('-q', '--query', type=str, help='Query to database', required=True)
    return parser.parse_args(sys.argv[1:])

def load_tensors(embedding_dir : str)-> Tuple[List[torch.Tensor], Dict[int, str]]:
    list_tensor = []
    dict_with_indexes = {}
    emb_dir_path = Path(embedding_dir).absolute()

    if (not emb_dir_path.exists()):
        print(f"{emb_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    index = 0
    for filename_short in os.listdir(emb_dir_path.as_posix()):
        filename = os.path.join(emb_dir_path.as_posix(), filename_short)
        list_tensor.append(torch.load(filename, weights_only=True))
        dict_with_indexes[index] = filename_short.split(".pt")[0]
        index += 1

    return (list_tensor, dict_with_indexes)

def embed_query(query : str) -> torch.Tensor:
    embedding = SBertEmbedding()
    return embedding.get(query)


def main() -> None:

    args = parse_args()
    (tensor_list, dict_with_indexes) = load_tensors(EMBEDDING_DIR)
    tensors = np.vstack(tensor_list)
    cos_similarities = cosine_similarity(tensors)

    emb_query = embed_query(args.query)
    print(f"User query: {args.query}")
    query_similarities = cosine_similarity([emb_query[0]], tensors)[0]

    #most_similar_index = np.argmax(query_similarities)
    similarity_list = []
    for index in range(len(dict_with_indexes)):
        similarity_list.append((dict_with_indexes[index], query_similarities[index]))

    similarity_list.sort(key=lambda x: x[1], reverse=True)
    print(similarity_list)

    #print(f"Most_simular_file = #{dict_with_indexes[most_similar_index]}#")


if __name__ == "__main__":
    main()