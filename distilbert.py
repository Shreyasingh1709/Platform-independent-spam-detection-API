from transformers import pipeline

# Load pretrained model
classifier = pipeline("text-classification", model="distilbert-base-uncased")

# Test example
result = classifier("You have won free money!")
print(result)