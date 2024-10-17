# import Simulationmain
from Simulation import Procedures
import matplotlib.pyplot as plt

def create_dict_procedures():
    procedures = Procedures.create_procedures()
    return {p.name: [0, 0] for p in procedures}

def procedure_most_used(hospital):
    # Ordenar los procedures por los que mas uses tengan
    procedures = sorted(hospital.procedures, key=lambda p: p.uses, reverse=True)

    # Crear diccionario de procedures con los datos de la simulacion
    # procedure.name: [procedure.uses, procedure.most_used]
    procedures_dict = {p.name: [p.uses, 0] for p in procedures}
    procedures_dict[procedures[0].name][1] = 1

    return procedures_dict

def test_procedures(func, num_sims=10):
    test_dict = {}
    general_dict = create_dict_procedures()
    procs = general_dict.keys()
    
    for i in range(0, 31, 1):
        aux = {}
        for j in range(num_sims):
            print(f"Simulate threshold = {i}")
            hospital = func(i)
            procedure_dict = procedure_most_used(hospital)
            # Combinar ambos diccionarios sumando los valores
            for key in procs:
                aux[key] = [
                    general_dict[key][0] + procedure_dict[key][0],  # Sumar los uses de cada array
                    general_dict[key][1] + procedure_dict[key][1]   # Sumar los most_used valores de cada array
                ]
        test_dict[i] = aux

    return test_dict

def graphs(data, value_to_graph, num_sims=10): # value_to_graph: 0 => uses, 1 => most_used
    mi_diccionario = [v for k, v in data.items()]

    labels = []
    values = []
    
    for element in mi_diccionario:
        
        diccionario_ordenado = sorted(element.items(), key=lambda x: x[1][value_to_graph], reverse=True)

        # Guardar el primer valor (el array completo) en una variable
        clave, valor = diccionario_ordenado[0]  # Obtiene el array completo del primer elemento
        labels.append(clave)
        values.append(valor[value_to_graph])

    # Obtener las diferencias entre cada par consecutivo de valores
    differences = [values[i] - values[i-1] for i in range(1, len(values))]

    # Agregar el primer valor al inicio, ya que no tiene un previo con el cual restar
    differences.insert(0, values[0])

    # Generar los thresholds de 5 a 100
    thresholds = [f'threshold {i}: {labels[int((i))]}' for i in range(0, 31, 1)]

    # Crear gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(thresholds, values)

    # Agregar etiquetas y título
    plt.xlabel('Thresholds', fontsize=12)
    plt.ylabel('Values', fontsize=12)
    plt.title('Values by Thresholds', fontsize=14)

    # Rotar las etiquetas del eje x para mejor legibilidad
    plt.xticks(rotation=45)

    # Mostrar gráfico
    plt.tight_layout()
    plt.savefig(f"Informe/most_used_service.png")
    plt.close()  # Cerrar la figura para no mostrarla en pantalla

