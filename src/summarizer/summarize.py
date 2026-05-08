# Simple summarization without heavy dependencies
def generate_summary(text):
    if not text:
        return "No text provided for summarization."

    # Simple extractive summary: take first few sentences
    sentences = text.split('.')
    summary_sentences = sentences[:3]  # Take first 3 sentences
    summary = '. '.join([s.strip() for s in summary_sentences if s.strip()])
    if not summary.endswith('.'):
        summary += '.'
    return summary[:200] + '...' if len(summary) > 200 else summary


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
