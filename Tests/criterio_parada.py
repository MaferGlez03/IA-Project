import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

def test_procedures(func, num_sims=10):
    test_dict = {}
    for i in range(0, 101, 5):
        prom = 0
        for j in range(num_sims):
            print(f"Simulate threshold = {i}")
            hospital = func(i)
            prom += hospital.patients_treated
        test_dict[f"progress disease level {i}"] = prom / num_sims
    
    return test_dict

def graphs(data):
    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='skyblue')

    # Añadir títulos y etiquetas
    plt.title('Pacientes atendidos por criterio de parada')
    plt.xlabel('Criterio de parada')
    plt.ylabel('Promedio pacientes atendidos')
    plt.xticks(rotation=45)  # Rotar etiquetas en el eje X para mejor visualización

    # Mostrar gráfico
    plt.tight_layout()  # Ajustar el gráfico para que se vea bien con las etiquetas largas
    plt.savefig(f"Informe/patients_treated_by_stop_criteria.png")
    plt.close()  # Cerrar la figura para no mostrarla en pantalla

def statistics(data):
    # Inicializar listas para la cantidad de pacientes atendidos y probabilidad de empeorar
    patients_attended = []
    worsening_probabilities = []

    # Extraer la cantidad de pacientes y la probabilidad de empeorar de cada nivel
    for level in data.keys():
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

    # Interpretar los resultados
    alpha = 0.05  # Nivel de significancia
    if p_value < alpha:
        print(f"El valor p es {p_value}, lo cual es menor que el nivel de significancia de {alpha}.")
        print("Existe una diferencia significativa entre la cantidad de pacientes atendidos y la probabilidad de empeorar.")
    else:
        print(f"El valor p es {p_value}, lo cual es mayor o igual al nivel de significancia de {alpha}.")
        print("No existe una diferencia significativa entre la cantidad de pacientes atendidos y la probabilidad de empeorar.")

    # Visualizar los datos
    visualize_data(patients_attended, worsening_probabilities)

def visualize_data(patients_attended, worsening_probabilities):
    # Crear un gráfico de distribución de los datos
    plt.figure(figsize=(10, 6))

    # Crear un boxplot para mostrar la distribución de ambas variables
    sns.boxplot(data=[patients_attended, worsening_probabilities], palette="Set2")
    plt.xticks([0, 1], ['Patients Attended', 'Worsening Probabilities'])
    plt.title("Distribución de pacientes atendidos y probabilidades de empeorar")

    # Mostrar el gráfico
    plt.tight_layout()
    plt.savefig(f"Informe/boxplot_distribution.png")
    plt.close()  # Cerrar la figura para no mostrarla en pantalla

    # Graficar las distribuciones de cada conjunto de datos
    plt.figure(figsize=(10, 6))
    sns.histplot(patients_attended, kde=True, color='blue', label='Patients Attended', bins=10)
    sns.histplot(worsening_probabilities, kde=True, color='red', label='Worsening Probabilities', bins=10)

    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('Distribución de Pacientes Atendidos y Probabilidades de Empeorar')

    plt.tight_layout()
    plt.savefig(f"Informe/histogram_distribution.png")
    plt.close()  # Cerrar la figura para no mostrarla en pantalla