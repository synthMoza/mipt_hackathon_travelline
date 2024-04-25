#! /usr/bin/env python3


from travelline.backend.database.database_implementation import EmbeddingsDB
from travelline.backend.rag.sbertembedding import SBertEmbedding
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

import torch
import numpy as np

class DB_Searcher():

    def __init__(self, db : EmbeddingsDB) -> None:
        self.db :EmbeddingsDB = db
        self.embedding_creator : SBertEmbedding = SBertEmbedding()
        self.real_question_embedding : torch.Tensor = torch.tensor(1024)

    def ask_real_question(self, query : str) -> None:
        self.real_question_embedding = torch.nn.functional.normalize(self.embedding_creator.get(query))

    def get_full_simularity_list(self) -> List[Tuple[int, float]]:

            id_tensor_pairs = self.db.get_all_embeddings()
            ids = [x[0] for x in id_tensor_pairs]
            tensors = [x[1] for x in id_tensor_pairs]
            tensors = np.vstack(tensors)
            query_similarities = cosine_similarity([self.real_question_embedding[0]], tensors)[0]

            simularity_list = []
            for id, probability in zip(ids, query_similarities):
                 simularity_list.append((id, probability))
            simularity_list.sort(key=lambda x: x[1], reverse=True)

            return simularity_list
    
    def get_reduced_simularity_list(self, N : int) -> List[Tuple[int, float]]:

        if (N < 1):
             print("get_reduced_simularity_list: N should be positive, exiting!")
             self.close_db()
             exit(-1)
        return self.get_full_simularity_list()[: N]
    
    def close_db(self) -> None:
         self.db.disconnect_db()






