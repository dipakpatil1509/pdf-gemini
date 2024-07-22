from transformers import BertModel, BertTokenizer
import numpy as np
from sklearn.neighbors import NearestNeighbors
import torch


class SemanticSearch:

    ENCODER_MODEL = None
    ENCODER_TOKENIZER = None

    def __init__(self):
        if self.ENCODER_MODEL == None or self.ENCODER_TOKENIZER == None:
            # self.ENCODER_MODEL = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
            model_name = "bert-base-uncased"
            self.ENCODER_TOKENIZER = BertTokenizer.from_pretrained(model_name)
            self.ENCODER_MODEL = BertModel.from_pretrained(model_name)

        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def get_text(self, text, return_data=True):
        # inp_emb = self.ENCODER_MODEL.encode([text])
        inp_emb = self.get_text_embedding(text).reshape(1, -1)
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]
        print("Neightbors", neighbors)
        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors
        
    def get_embedding(self, text):
        inputs = self.ENCODER_TOKENIZER(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.ENCODER_MODEL(**inputs)
        # Use the embeddings from the [CLS] token
        embeddings = outputs.last_hidden_state[:, 0, :].squeeze()
        return embeddings
    
    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i : (i + batch)]
            # Use the embeddings from the [CLS] token
            embeddings.append(self.get_embedding(text_batch))
            # embeddings.append(emb_batch)
        embeddings_matrix = np.vstack(embeddings)
        # embeddings_matrix = torch.stack(embeddings).numpy()
        return embeddings_matrix
