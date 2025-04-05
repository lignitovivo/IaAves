import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import numpy as np  # Asegúrate de importar esto

# Cargar el CSV
df = pd.read_csv("perfiles_acusticos.csv")

# Separar características y etiquetas
X = df.drop(columns=["especie"])
y = df["especie"]

# Codificar etiquetas de texto a números
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluar el modelo
y_pred = modelo.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# Solución al error: usar solo las etiquetas presentes en y_test
etiquetas_presentes = np.unique(y_test)
print("📊 Reporte de clasificación:\n", classification_report(
    y_test,
    y_pred,
    labels=etiquetas_presentes,
    target_names=le.inverse_transform(etiquetas_presentes)
))

# Guardar modelo y codificador
joblib.dump(modelo, "modelo_aves.pkl")
joblib.dump(le, "codificador_etiquetas.pkl")
