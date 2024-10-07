import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer

class DiseasePredictionModel:
    def __init__(self, ontology, csv_file):
        self.ontology = ontology
        self.data = pd.read_csv(csv_file)
        self.model = None
        self.models = None  # Para almacenar los modelos entrenados
        self.symptom_map = self.create_symptom_map()
        self.mlb = MultiLabelBinarizer()

    def create_symptom_map(self):
        # Crear un diccionario de síntomas a partir de la ontología
        symptom_map = {}
        for symptom in self.ontology['symptoms']:
            symptom_map[symptom['name']] = symptom['id']
        return symptom_map

    def preprocess_data(self):
        df = self.data
        df['symptoms'] = df['symptoms'].apply(lambda x: x.split(', '))
        symptom_features = self.mlb.fit_transform(df['symptoms'])
        symptom_columns = [f"{symptom}" for symptom in self.mlb.classes_]

        # Combinar las nuevas columnas con el DataFrame original
        df_symptoms = pd.DataFrame(symptom_features, columns=symptom_columns)
        df = pd.concat([df, df_symptoms], axis=1)

        # Eliminar la columna original de síntomas
        df = df.drop(columns=['symptoms'])

        # Separar las características de las etiquetas (diagnósticos)
        X = df.drop(columns=['Brain_Cancer', 'Encephalitis', 'Epilepsy', 'Multiple_Sclerosis', 'Prion_Diseases',
                     'Spinal_Muscular_Atrophy', 'Parkinson_Disease', 'Lewy_Body_Dementia',
                     'Huntington_Disease', 'Friedreich_Ataxia', 'Amyotrophic_Lateral_Sclerosis',
                     'Alzheimer_Disease'])
        
        # La etiqueta será la enfermedad correspondiente
        y = df[['Brain_Cancer', 'Encephalitis', 'Epilepsy', 'Multiple_Sclerosis', 'Prion_Diseases',
                     'Spinal_Muscular_Atrophy', 'Parkinson_Disease', 'Lewy_Body_Dementia',
                     'Huntington_Disease', 'Friedreich_Ataxia', 'Amyotrophic_Lateral_Sclerosis',
                     'Alzheimer_Disease']]

        return X, y

    def train_model(self):
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar un modelo RandomForest para cada enfermedad
        models = {}
        for disease in y.columns:
            model = RandomForestClassifier()
            model.fit(X_train, y_train[disease])
            models[disease] = model

        self.models = models  # Guardar los modelos entrenados

        # Realizar predicciones
        predictions = {}
        for disease, model in models.items():
            predictions[disease] = model.predict(X_test)

        # Medir la precisión de cada modelo
        for disease in predictions:
            acc = accuracy_score(y_test[disease], predictions[disease])

    def predict_disease(self, symptom_list):
        # Crear un vector de características a partir de los síntomas proporcionados
        symptom_features = self.mlb.transform([symptom_list])  # La función transform requiere una lista de listas
        symptom_columns = [f"Symptom_{symptom}" for symptom in self.mlb.classes_]
        input_vector = pd.DataFrame(symptom_features, columns=symptom_columns)

        # Llenar con ceros las columnas que faltan en input_vector
        missing_cols = set(self.models[list(self.models.keys())[0]].feature_names_in_) - set(input_vector.columns)
        for col in missing_cols:
            input_vector[col] = 0

        # Ordenar las columnas para que coincidan con el entrenamiento
        input_vector = input_vector[self.models[list(self.models.keys())[0]].feature_names_in_]

        # Predecir enfermedades
        predicted_diseases = {}
        for disease, model in self.models.items():
            prediction = model.predict(input_vector)
            predicted_diseases[disease] = prediction

        # Aplicar operación a cada valor y crear un nuevo diccionario
        diccionario_modificado = {clave: int(valor[0][:-1]) for clave, valor in predicted_diseases.items()}

        # Ordenar el diccionario modificado por valor
        final = dict(sorted(diccionario_modificado.items(), key=lambda x: x[1], reverse=True))

        return final




