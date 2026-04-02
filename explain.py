import shap
import numpy as np
from preprocess import preprocess_text

# This will be set from main.py
explainer = None
vectorizer = None

def initialize_explainer(model, vec):
    global explainer, vectorizer
    vectorizer = vec
    
    def predict_proba(texts):
        cleaned = [preprocess_text(t) for t in texts]
        vectors = vec.transform(cleaned)
        return model.predict_proba(vectors)
    
    explainer = shap.Explainer(predict_proba, vec.transform(["dummy text"]))

def get_shap_explanation(text):
    if explainer is None:
        return ["Explainer not initialized"]

    try:
        shap_values = explainer([text])
        # Get feature names (words)
        feature_names = vectorizer.get_feature_names_out()
        # Get SHAP values
        values = shap_values.values[0]
        # Get top contributing words
        top_indices = np.argsort(np.abs(values))[-3:]
        keywords = [feature_names[i] for i in top_indices]
        return keywords
    except:
        return ["Unable to compute explanation"]
