from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

# Load AI summarization model
summarizer = pipeline("summarization")

def generate_summary(text):

    result = summarizer(
        text,
        max_length=80,
        min_length=25,
        do_sample=False
    )

    return result[0]['summary_text']


def extract_keywords(text, top_n=8):
    if not text or not text.strip():
        return []

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.85)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    if len(scores) == 0:
        return []

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    keywords = [feature_names[i] for i in top_indices if feature_names[i].strip()]
    return keywords
