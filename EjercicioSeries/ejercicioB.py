archivo_texto= "./catalog.csv"
from datetime import datetime

def numero_invalido(valor):
    try:
        numero_float = float(valor)
        numero = int(numero_float)
        if numero <= 0:
            return True
        return False
    except (ValueError, TypeError):
        return True

def calcular_puntaje(episodio):
    resultado = 0

    if episodio[4] != "Unknown":
        resultado += 3

    if episodio[3] != "Untitled Episode":
        resultado += 2

    if episodio[1] != 0 and episodio[2] != 0:
        resultado += 1
    return resultado

def validar_fecha(fecha_texto):
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%Y/%m/%d"]
    for fmt in formatos:
        try:
            datetime.strptime(fecha_texto, fmt)
            return True
        except ValueError:
            continue
    return False

if __name__ == '__main__':

    valores_nulos = ["Unknown","unknown", 0, '', " "]

    catalogo = {}
    total_entrada = 0
    descartados = 0
    corregidos = 0
    duplicados = 0

    with open(archivo_texto, 'r', encoding='utf-8') as archivo:

        for linea in archivo:

            total_entrada += 1

            columnas = linea.strip().split(';')
            while len(columnas) < 5:
                columnas.append("")
            if columnas[0].strip() in valores_nulos:
                descartados += 1
                continue

            columnas[0] = " ".join(columnas[0].strip().lower().split())
            serie_normalizada = columnas[0]

            if columnas[1].strip() in valores_nulos or numero_invalido(columnas[1]):
                columnas[1] = 0
                corregidos += 1
            else:
                columnas[1] = int(float(columnas[1]))

            if columnas[2].strip() in valores_nulos or numero_invalido(columnas[2]):
                columnas[2] = 0
                corregidos += 1
            else:
                columnas[2] = int(float(columnas[2]))

            if columnas[3].strip() in valores_nulos:
                columnas[3] = "Untitled Episode"

            columnas[3] = " ".join(columnas[3].strip().lower().split())
            titulo_normalizado = columnas[3]

            if not validar_fecha(columnas[4]):
                columnas[4] = "Unknown"
                corregidos += 1

            if columnas[2] == 0 and columnas[3] == "Untitled Episode" and columnas[4] == "Unknown":
                descartados += 1
                continue

            clave1 = (serie_normalizada, columnas[1], columnas[2])
            clave2 = (serie_normalizada, 0, columnas[2], titulo_normalizado)
            clave3 = (serie_normalizada, columnas[1], 0, titulo_normalizado)

            registro = [columnas[0], columnas[1], columnas[2], columnas[3], columnas[4]]

            encontrado = None

            for clave in [clave1, clave2, clave3]:
                if clave in catalogo:
                    encontrado = clave
                    break

            if encontrado:
                duplicados += 1

                if calcular_puntaje(registro) > calcular_puntaje(catalogo[encontrado]):
                    catalogo[encontrado] = registro
            else:
                catalogo[clave1] = registro


    with open("episodes_clean.csv", "w", encoding="utf-8") as salida:

        episodios_ordenados = sorted(catalogo.values(),key=lambda x: (x[0], x[1], x[2]) )
        salida.write("SeriesName,SeasonNumber,EpisodeNumber,EpisodeTitle,AirDate\n")

        for e in episodios_ordenados:
            salida.write(f"{e[0]},{e[1]},{e[2]},{e[3]},{e[4]}\n")


    with open("report.md", "w", encoding="utf-8") as reporte:
        reporte.write("# Data Quality Report\n\n")
        
        reporte.write(f"Total input records: {total_entrada} \n")
        reporte.write(f"Total output records: {len(catalogo)} \n")
        reporte.write(f"Discarded entries: {descartados} \n")
        reporte.write(f"Corrected entries: {corregidos} \n")
        reporte.write(f"Duplicates detected: {duplicados} \n\n")

        reporte.write("## Deduplication Strategy\n\n")
        reporte.write("Duplicate episodes are detected using three alternative keys based on normalized fields.\n\n")
        reporte.write("Once a duplicate is detected, the script selects the best record using a scoring function"
                      " called `calcular_puntaje`.\n")
        reporte.write("This function implements the priority rules defined in the specification by assigning"
                      "a weighted score to each record.\n")
        reporte.write("The weights reflect the order of importance described in the problem statement.\n\n")

        reporte.write("Scoring criteria:\n\n")
        reporte.write("- Episodes with a valid AirDate receive the highest priority over those with 'Unknown'.\n")
        reporte.write("- Episodes with a known title are preferred over those labeled 'Untitled Episode'.\n")
        reporte.write("- Episodes with valid Season and Episode numbers receive additional priority.\n\n")

        reporte.write("When two duplicate records are found, their scores are compared and the record with the higher"
                      " score is kept.\n")
        reporte.write("If both records have the same score, the first occurrence in the dataset is preserved.\n")