import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import os

ruta = os.path.join("data", "raw", "learning_style_vak.csv")
df = pd.read_csv(ruta)

print("Primeras filas del dataset original:")
print(df.head())

print("\nEstilos únicos:", df['Type'].unique())

df = df.dropna(subset=['Sentence', 'Type'])

df = df.sample(n=3000, random_state=42)

X = df['Sentence'] 
y = df['Type']  

vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

os.makedirs("model", exist_ok=True)
joblib.dump(vectorizer, "model/vectorizer_vak.pkl")

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

joblib.dump((X_train, y_train), "model/vak_train.pkl")
joblib.dump((X_test, y_test), "model/vak_test.pkl")

print("\n✅ Dataset VAK procesado y guardado con éxito.")
