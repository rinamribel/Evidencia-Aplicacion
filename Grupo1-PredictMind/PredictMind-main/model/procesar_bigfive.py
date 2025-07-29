import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import os

ruta = os.path.join("data", "raw", "bigfive_responses.csv")

df = pd.read_csv(ruta, sep="\t", nrows=5000)

print("Columnas del dataset:")
print(df.columns)

ext_cols = [f"EXT{i}" for i in range(1, 11)]
con_cols = [f"CSN{i}" for i in range(1, 11)] 

for col in ext_cols + con_cols:
    if col not in df.columns:
        raise Exception(f"Columna faltante: {col}")

df['extraversion'] = df[ext_cols].mean(axis=1)
df['conscientiousness'] = df[con_cols].mean(axis=1)

df['sociabilidad'] = pd.cut(df['extraversion'],
                            bins=[0, 3, 5, 7],
                            labels=['baja', 'media', 'alta'])

df['impulsividad'] = pd.cut(df['conscientiousness'],
                            bins=[0, 3, 5, 7],
                            labels=['alta', 'media', 'baja'])

df = df.dropna(subset=['sociabilidad', 'impulsividad'])

X = df[ext_cols + con_cols]
y_sociabilidad = df['sociabilidad']
y_impulsividad = df['impulsividad']

X_train_soc, X_test_soc, y_train_soc, y_test_soc = train_test_split(
    X, y_sociabilidad, test_size=0.2, random_state=42)

X_train_imp, X_test_imp, y_train_imp, y_test_imp = train_test_split(
    X, y_impulsividad, test_size=0.2, random_state=42)

joblib.dump((X_train_soc, y_train_soc), "model/sociabilidad_train.pkl")
joblib.dump((X_test_soc, y_test_soc), "model/sociabilidad_test.pkl")
joblib.dump((X_train_imp, y_train_imp), "model/impulsividad_train.pkl")
joblib.dump((X_test_imp, y_test_imp), "model/impulsividad_test.pkl")

print("\n✅ Dataset Big Five procesado y guardado con éxito.")
