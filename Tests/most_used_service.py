from Simulationmain import create_procedures, run_simulation
import matplotlib.pyplot as plt

def create_dict_procedures():
    procedures = create_procedures()
    return {p.name: [0, 0] for p in procedures}

def procedure_most_used(hospital):
    # Ordenar los procedures por los que mas uses tengan
    procedures = sorted(hospital.procedures, key=lambda p: p.uses, reverse=True)

    # Crear diccionario de procedures con los datos de la simulacion
    # procedure.name: [procedure.uses, procedure.most_used]
    procedures_dict = {p.name: [p.uses, 0] for p in procedures}
    procedures_dict[procedures[0].name][1] = 1

    return procedures_dict

def test_procedures():
    test_dict = {}
    for i in range(5, 101, 5):
        general_dict = create_dict_procedures()
        for j in range(100):
            hospital = run_simulation(i)
            procedure_dict = procedure_most_used(hospital)
            # Combinar ambos diccionarios sumando los valores
            for key in general_dict:
                general_dict[key] = [
                    general_dict[key][0] + procedure_dict[key][0],  # Sumar los uses de cada array
                    general_dict[key][1] + procedure_dict[key][1]   # Sumar los most_used valores de cada array
                ]
        test_dict[f"progress disease level {i}": general_dict]
    
    return test_dict

def graphs(data, value_to_graph): # value_to_graph: 0 => uses, 1 => most_used
    # Inicializar listas para almacenar los datos
    levels = []
    procedures = []
    int1_values = []

    # Extraer los datos del diccionario
    for level, procedures_dict in data.items():
        for procedure, values in procedures_dict.items():
            levels.append(level)
            procedures.append(f"{level} - {procedure}")
            int1_values.append(values[value_to_graph])  # int1 es el primer valor del array

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(procedures, int1_values, color='skyblue')

    # Añadir títulos y etiquetas
    plt.title('Valores de int1 por Procedure y Progress Disease Level')
    plt.xlabel('Procedures por Progress Disease Level')
    if value_to_graph:
        plt.ylabel('Procedure most used')
    else:
        plt.ylabel('Uses by procedure')
    plt.xticks(rotation=90)  # Rotar etiquetas en el eje X para mejor visualización

    # Mostrar gráfico
    plt.tight_layout()  # Ajustar el gráfico para que se vea bien con las etiquetas largas
    plt.show()

