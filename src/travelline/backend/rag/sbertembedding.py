from embedding import AbstractEmbedding

from transformers import AutoTokenizer, AutoModel
import torch

model_id = "ai-forever/sbert_large_nlu_ru"

class SBertEmbedding(AbstractEmbedding):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id)
    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask
    def get(self, text: str):
        encoded_input = self.tokenizer(text, padding=True, truncation=True, max_length=24, return_tensors='pt')

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        sentence_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings