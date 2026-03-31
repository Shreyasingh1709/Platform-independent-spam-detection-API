# explain.py

# Use the same preprocessing as model_training.py
from preprocess import preprocess_text

# example spam keyword list
spam_words = {
    "free","win","winner","cash","prize","offer",
    "click","buy","urgent","money","claim",
    "credit","loan","cheap","discount"
}

def get_keywords(text):
    cleaned = preprocess_text(text)
    words = cleaned.split()
    # keep words that match spam keywords
    keywords = [word for word in words if word in spam_words]
    # return top 3 words
    return list(set(keywords))[:3]