import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def retrieve(question, index, chunks):

    question_embedding = model.encode([question])
    top_k = min(3, len(chunks))
    distances, indices = index.search(
        np.array(question_embedding).astype("float32"),
        3
    )

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results