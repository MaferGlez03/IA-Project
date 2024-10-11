def save_log(results):
    # Abre (o crea) el archivo en modo escritura ('w'), que sobrescribe el archivo si ya existe
    with open("log.txt", "w") as file:
        # Recorre cada tupla en el array y escribe cada una en una línea nueva
        for result in results:
            file.write(f"{result[0]}, {result[1]}\n")