import gensim
import numpy as np
from gensim.matutils import unitvec

MODEL_NAME = ""

words = []
vectors = np.array([])
word_vectors = {}


def load_model():
    global words, vectors, word_vectors
    model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_NAME, binary=True)
    words = [w for w in model.index_to_key if w.lower() == w]
    vectors = np.array([unitvec(model[w]) for w in words])
    word_vectors = {k: v for k, v in zip(words, vectors)}


load_model()
print(words)
