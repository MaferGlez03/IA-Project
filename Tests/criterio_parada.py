import numpy as np
import scipy.stats as stats
from Simulationmain import run_simulation
import matplotlib.pyplot as plt

def test_procedures():
    test_dict = {}
    for i in range(0, 101, 5):
        prom = 0
        for j in range(100):
            hospital = run_simulation(i)
            prom += hospital.patients_treated
        test_dict[f"progress disease level {i}": prom/100]
    
    return test_dict

def graphs(data):
    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='skyblue')

    # Añadir títulos y etiquetas
    plt.title('Pacientes atendidos por criterio de parada')
    plt.xlabel('Criterio de parada')
    plt.ylabel('Promedio pacientes atendidos')
    plt.xticks(rotation=90)  # Rotar etiquetas en el eje X para mejor visualización

    # Mostrar gráfico
    plt.tight_layout()  # Ajustar el gráfico para que se vea bien con las etiquetas largas
    plt.show()

def statistics(data):
    # Inicializar listas para la cantidad de pacientes atendidos y probabilidad de empeorar
    patients_attended = []
    worsening_probabilities = []

    # Extraer la cantidad de pacientes y la probabilidad de empeorar de cada nivel
    for level in data:
        # Obtener el valor numérico del nivel del progreso (e.g., 5, 10, 15, etc.)
        worsening_prob = int(level.split()[-1])  # Extraer '5', '10', '15', etc.
        
        # Cantidad de pacientes atendidos es el valor en el diccionario
        attended = data[level]
        
        # Agregar a las listas
        worsening_probabilities.append(worsening_prob)
        patients_attended.append(attended)

    # Realizar la prueba de Mann-Whitney U
    mannwhitney_stat, p_value = stats.mannwhitneyu(patients_attended, worsening_probabilities, alternative='two-sided')

    # Mostrar resultados
    print(f"Estadística de Mann-Whitney U: {mannwhitney_stat}")
    print(f"Valor p de la prueba: {p_value}")