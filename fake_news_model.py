# fake_news_model.py
import random

def predict_fake_news(text):
    """
    Dummy fake news detector.
    Replace with your ML model (e.g., TF-IDF + Logistic Regression).
    """
    labels = ["Real", "Fake", "Uncertain"]
    prediction = random.choice(labels)
    confidence = round(random.uniform(0.7, 0.99), 2)
    
    return prediction, confidence
