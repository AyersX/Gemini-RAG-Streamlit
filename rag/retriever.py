from config.settings import TOP_K_RETRIEVAL, THRESHOLD
from rag.embedd import Embedding


class Retriever:
  def __init__(self):
    self.model = Embedding().getmodel()

  def retrieve(self, query=None, index=None, chunks=None, top_k=TOP_K_RETRIEVAL):
    if query and index and chunks:
      query_format = f"query: {query}"
      query_vector = self.model.encode([query_format])
      # print(f"max token model: {self.model.max_seq_length} tokens")

      distance, indices = index.search(query_vector, top_k)

      result = ""
      for idx, dist in zip(indices[0], distance[0]):
        if idx != -1:
          if dist <= THRESHOLD:
            result += chunks[idx] + "\n\n"
            print(f"\nrelevant data: \n{dist}")
          else:
            print(f"\nout of distance: \n{dist}")
      return result

    else:
      print("skip RAG")
