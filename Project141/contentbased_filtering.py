from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

df = pd.read_csv('shared_articles.csv')
df = df[df['title'].notna()]

count = CountVectorizer(stop_words='english')
countMatrix = count.fit_transform(df['title'])

cosine_sim2 = cosine_similarity(countMatrix, countMatrix)

df = df.reset_index()
indices = pd.Series(df.index, index=df['contentId'])


def getRecommendations(contentId):
    idx = indices[int(contentId)]
    sim_scores = list(enumerate(cosine_sim2[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    article_indices = [i[0] for i in sim_scores]
    return df[["url", "title", "text", "lang", "total_events"]].iloc[article_indices].values.tolist()