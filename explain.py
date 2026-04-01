import shap
import numpy as np

# This will be set from main.py
explainer = None
vectorizer = None

def initialize_explainer(model, vec):
    global explainer, vectorizer
    vectorizer = vec
    explainer = shap.Explainer(model, vec.transform)

def get_shap_explanation(text):
    if explainer is None:
        return ["Explainer not initialized"]

    shap_values = explainer([text])

    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()

    # Get SHAP values
    values = shap_values.values[0]

    # Get top contributing words
    top_indices = np.argsort(np.abs(values))[-3:]

    keywords = [feature_names[i] for i in top_indices]

    return keywords
