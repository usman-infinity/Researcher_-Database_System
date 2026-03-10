from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_papers(papers, current_title):

    titles = [paper.title for paper in papers]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(titles)

    similarity = cosine_similarity(tfidf_matrix)

    index = titles.index(current_title)

    scores = list(enumerate(similarity[index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommended = []

    for i in scores[1:6]:
        recommended.append(papers[i[0]])

    return recommended