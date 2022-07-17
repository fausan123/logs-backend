import joblib
from sklearn.metrics.pairwise import cosine_similarity

def suggest_lo(sentences):
    model = joblib.load('.\mlmodels\sentence_model.sav')
    embeddings = model.encode(sentences)
    arr = list(cosine_similarity([embeddings[0]], embeddings[1:])[0])
    index = arr.index(max(arr))
    return sentences[index+1]