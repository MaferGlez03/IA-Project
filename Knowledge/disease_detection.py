import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.multioutput import MultiOutputClassifier

class DiseasePredictionModel:
    def __init__(self, ontology, csv_file):
        self.ontology = ontology
        self.data = pd.read_csv(csv_file)
        self.model = None
        self.symptom_map = self.create_symptom_map()

    def create_symptom_map(self):
        # Crear un diccionario de síntomas a partir de la ontología
        symptom_map = {}
        for symptom in self.ontology['symptoms']:
            symptom_map[symptom['name']] = symptom['id']
        return symptom_map

    def preprocess_data(self):
        # Convertir los síntomas de cada paciente en características binarias
        all_symptoms = [symptom['name'] for symptom in self.ontology['symptoms']]
        for symptom in all_symptoms:
            self.data[symptom] = self.data['symptoms'].apply(lambda x: 1 if symptom in x else 0)

        diagnosis_columns = [f'diagnosis{i}' for i in range(1, 13)]

        # Definir X (características)
        X = self.data.drop(['patient_id', 'symptoms'] + diagnosis_columns, axis=1)

        # Crear la etiqueta de enfermedad como DataFrame
        y = self.data[diagnosis_columns].copy()  # Copiar las columnas de diagnóstico directamente

        return X, y

    def train_model(self):
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Usar MultiOutputClassifier con RandomForest
        self.model = MultiOutputClassifier(RandomForestClassifier(random_state=42))
        self.model.fit(X_train, y_train)
        
        # Evaluar el modelo
        y_pred = self.model.predict(X_test)
        
        # Calcular la precisión por enfermedad
        accuracy = (y_pred == y_test.values).mean(axis=0)  # Promedio de precisión por enfermedad
        for i, acc in enumerate(accuracy):
            print(f"Accuracy for Disease {i + 1}: {acc * 100:.2f}%")
    
    def predict(self, patient_symptoms, patient_info):
        # Crear un vector para los síntomas del paciente
        symptoms_vector = [1 if symptom in patient_symptoms else 0 for symptom in self.symptom_map]

        # Crear un vector para los factores del paciente
        factors_vector = []
        for factor in ['lifestyle_factors', 'family_history', 'genetic_predisposition', 'environmental_exposure']:
            for i in range(1, 13):
                factors_vector.append(f"{factor}{i}")  # Se espera que sea 0 o 1

        # Concatenar síntomas e información adicional
        features = list(patient_info.values()) + symptoms_vector

        # Crear un DataFrame con nombres de características
        feature_names = ['age'] + factors_vector + list(self.symptom_map.keys())
        features_df = pd.DataFrame([features], columns=feature_names)

        
        # Obtener las predicciones para todas las enfermedades
        predictions = self.model.predict(features_df)[0]  # Obtiene un vector de 12 elementos
        
        return predictions

