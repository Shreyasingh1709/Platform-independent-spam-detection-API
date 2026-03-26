import re
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def preprocess_text(text):
    
    # convert to lowercase
    text = text.lower()
    
    # remove numbers
    text = re.sub(r'\d+', '', text)
    
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # remove extra spaces
    text = text.strip()
    
    # remove stopwords
    words = text.split()
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]
    
    cleaned_text = " ".join(words)
    
    return cleaned_text