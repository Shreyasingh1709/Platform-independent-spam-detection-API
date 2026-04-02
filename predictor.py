import pickle
from preprocess import preprocess_text

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_spam(text):
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    return "spam" if prediction == 1 else "ham"

def get_confidence(text):
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    proba = model.predict_proba(vector)[0]
    return float(max(proba))