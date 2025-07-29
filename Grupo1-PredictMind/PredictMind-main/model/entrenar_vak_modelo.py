import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import os

X_train, y_train = joblib.load("model/vak_train.pkl")
X_test, y_test = joblib.load("model/vak_test.pkl")

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

print("🔍 Resultados de la evaluación:")
print(classification_report(y_test, y_pred))
print("✔️ Precisión general:", accuracy_score(y_test, y_pred))

joblib.dump(modelo, "model/modelo_vak.pkl")

print("\n✅ Modelo de estilo de aprendizaje entrenado y guardado con éxito.")
