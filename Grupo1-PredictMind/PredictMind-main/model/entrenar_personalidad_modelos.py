import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def entrenar_modelo(nombre, archivo_train, archivo_test, modelo_guardado):
    print(f"\n🔹 Entrenando modelo para: {nombre}")
    
    X_train, y_train = joblib.load(archivo_train)
    X_test, y_test = joblib.load(archivo_test)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("✔️ Precisión general:", accuracy_score(y_test, y_pred))

    # Guardar modelo
    joblib.dump(modelo, modelo_guardado)
    print(f"✅ Modelo de {nombre} guardado como {modelo_guardado}")

# Entrenar ambos modelos
entrenar_modelo(
    nombre="Sociabilidad",
    archivo_train="model/sociabilidad_train.pkl",
    archivo_test="model/sociabilidad_test.pkl",
    modelo_guardado="model/modelo_sociabilidad.pkl"
)

entrenar_modelo(
    nombre="Impulsividad",
    archivo_train="model/impulsividad_train.pkl",
    archivo_test="model/impulsividad_test.pkl",
    modelo_guardado="model/modelo_impulsividad.pkl"
)
