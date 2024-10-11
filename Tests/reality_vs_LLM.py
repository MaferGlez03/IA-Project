import numpy as np
import scipy.stats as stats
from Simulationmain import run_simulation
import matplotlib.pyplot as plt

def test_procedures():
    test_dict = {}
    for i in range(0, 101, 5):
        real_values = []
        llm_values = []
        for j in range(100):
            hospital = run_simulation(i)
            real_values.append(hospital.real)
            llm_values.append(hospital.llm)

        test_dict[f"progress disease level {i}": [real_values, llm_values]]
    
    return test_dict

def graphs(data):
    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), sum(data.values()[0]) / len(data.values()[0]), color='skyblue')
    plt.bar(data.keys(), sum(data.values()[1]) / len(data.values()[1]), color='red')

    # Añadir títulos y etiquetas
    plt.title('Resumen de promedios del LLM vs progreso real')
    plt.xlabel('Criterio de parada')
    plt.ylabel('LLM y progreso real')
    plt.xticks(rotation=90)  # Rotar etiquetas en el eje X para mejor visualización

    # Mostrar gráfico
    plt.tight_layout()  # Ajustar el gráfico para que se vea bien con las etiquetas largas
    plt.show()

def statistics_prom(data):
    # Inicializar listas para almacenar los promedios por nivel
    avg_progress_llm = []
    avg_progress_real = []

    # Calcular el promedio de cada lista de simulaciones por nivel
    for level in data:
        progress_llm_sim = data[level][0]
        progress_real_sim = data[level][1]
        
        # Promedio de progresos por nivel
        avg_llm = np.mean(progress_llm_sim)
        avg_real = np.mean(progress_real_sim)
        
        avg_progress_llm.append(avg_llm)
        avg_progress_real.append(avg_real)

    # Calcular la varianza de los promedios por nivel
    var_llm = np.var(avg_progress_llm)
    var_real = np.var(avg_progress_real)

    # Test de correlación de Spearman sobre los promedios por nivel
    spearman_corr, p_value = stats.spearmanr(avg_progress_llm, avg_progress_real)

    # Mostrar resultados
    print(f"Varianza de los progresos del LLM: {var_llm}")
    print(f"Varianza de los progresos reales: {var_real}")
    print(f"Correlación de Spearman: {spearman_corr}")
    print(f"Valor p del test de Spearman: {p_value}")

def statistics_general(data):
    # Inicializar listas para almacenar las varianzas por nivel
    variance_llm = []
    variance_real = []
    spearman_correlations = []

    # Calcular la varianza y la correlación para cada nivel
    for level in data:
        progress_llm_sim = data[level][0]
        progress_real_sim = data[level][1]
        
        # Calcular la varianza de los progresos del LLM y los progresos reales por simulación
        var_llm = np.var(progress_llm_sim)
        var_real = np.var(progress_real_sim)
        
        variance_llm.append(var_llm)
        variance_real.append(var_real)
        
        # Test de correlación de Spearman por simulación
        spearman_corr, _ = stats.spearmanr(progress_llm_sim, progress_real_sim)
        spearman_correlations.append(spearman_corr)

    # Calcular la varianza de las varianzas
    var_of_variances_llm = np.var(variance_llm)
    var_of_variances_real = np.var(variance_real)

    # Calcular la media de las correlaciones de Spearman
    avg_spearman_corr = np.mean(spearman_correlations)

    # Mostrar resultados
    print(f"Varianza de las varianzas de los progresos del LLM: {var_of_variances_llm}")
    print(f"Varianza de las varianzas de los progresos reales: {var_of_variances_real}")
    print(f"Promedio de las correlaciones de Spearman: {avg_spearman_corr}")