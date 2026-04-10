import joblib

model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_fake_news(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    confidence = max(model.predict_proba(X)[0])
    return prediction, round(confidence, 2)
