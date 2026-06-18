from config.settings import EMBEDDING_MODEL
from config.settings import FILE_INDEX_PATH

import faiss
import os
import numpy as np

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"


class Embedding:
  _model = None

  def __init__(self):
    if Embedding._model is None:
      from sentence_transformers import SentenceTransformer

      Embedding._model = SentenceTransformer(EMBEDDING_MODEL)
    self.MODEL = Embedding._model

  def getmodel(self):
    return self.MODEL

  def vector_index(self, chunks=None):
    if chunks:
      if os.path.getsize(FILE_INDEX_PATH) == 0:
        try:
          print(f"embedding {len(chunks)} chunks..")
          vector = self.MODEL.encode(chunks)
          vector = np.array(vector).astype("float32")

          dimension = vector.shape[1]
          index = faiss.IndexFlatL2(dimension)
          index.add(vector)
          faiss.write_index(index, str(FILE_INDEX_PATH))
          print("vector index success")
          return index
        except Exception as e:
          raise Exception(f"DEBUG VECTOR_INDEX: {e}")

      else:
        index = self.load_index()
        return index

    elif not chunks:
      raise ValueError("DEBUG VECTOR_INDEX: NONE")

  def load_index(self):
    if os.path.getsize(FILE_INDEX_PATH) > 0:
      index = faiss.read_index(str(FILE_INDEX_PATH))
      print("index already exists, return index")
      return index
    raise ValueError("DEBUG LOAD_INDEX: NONE")
