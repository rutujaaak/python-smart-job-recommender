from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(resume_text, job_data, top_n=3):
    job_descriptions = job_data['description'].tolist()
    corpus = [resume_text] + job_descriptions

    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform(corpus)

    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    top_indices = scores.argsort()[-top_n:][::-1]

    return job_data.iloc[top_indices], scores[top_indices]
