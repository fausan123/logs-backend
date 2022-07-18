from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity

def suggest_lo(sentences):
    model = settings.SENTENCE_MLMODEL
    embeddings = model.encode(sentences)
    arr = list(cosine_similarity([embeddings[0]], embeddings[1:])[0])
    index = arr.index(max(arr))
    return index