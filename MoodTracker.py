import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

data = {
    'text': ["I am happy",
             "I am sad",
             "I am upset"],
    'mood': ["positive",
             "negative",
             "neutral"]
}

df = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['mood'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

def predict_mood(user_input):
    user_input_tfidf = vectorizer.transform([user_input])
    prediction = model.predict(user_input_tfidf)
    return prediction[0]

user_input = input("Enter a sentence: ")
predicted_mood = predict_mood(user_input)
print(f"The predicted mood is: {predicted_mood}")