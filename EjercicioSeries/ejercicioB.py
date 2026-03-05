archivo_texto= "./catalog.csv"
from datetime import datetime

def limpiar_datos_numericos(valor):
    try:
        numero_float = float(valor)
        numero = int(numero_float)
        if numero <= 0:
            return True
        return False
    except (ValueError, TypeError):
        return True

def puntaje(episodio):
    resultado = 0

    if episodio[4] != "Unknown":
        resultado += 3

    if episodio[3] != "Untitled Episode":
        resultado += 2

    if episodio[1] != 0 and episodio[2] != 0:
        resultado += 1
    return resultado

def validar_formatos_fecha(fecha_texto):
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

            if columnas[1].strip() in valores_nulos or limpiar_datos_numericos(columnas[1]):
                columnas[1] = 0
                corregidos += 1
            else:
                columnas[1] = int(float(columnas[1]))

            if columnas[2].strip() in valores_nulos or limpiar_datos_numericos(columnas[2]):
                columnas[2] = 0
                corregidos += 1
            else:
                columnas[2] = int(float(columnas[2]))

            if columnas[3].strip() in valores_nulos:
                columnas[3] = "Untitled Episode"

            columnas[3] = " ".join(columnas[3].strip().lower().split())
            titulo_normalizado = columnas[3]

            if not validar_formatos_fecha(columnas[4]):
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

                if puntaje(registro) > puntaje(catalogo[encontrado]):
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
        
        reporte.write(f"Total input records: {total_entrada}\n")
        reporte.write(f"Total output records: {len(catalogo)}\n")
        reporte.write(f"Discarded entries: {descartados}\n")
        reporte.write(f"Corrected entries: {corregidos}\n")
        reporte.write(f"Duplicates detected: {duplicados}\n\n")
        
        reporte.write("## Deduplication Strategy\n\n")
        reporte.write("Episodes were considered duplicates when they matched one of the following keys:\n\n")
        reporte.write("- `(SeriesName_normalized, SeasonNumber, EpisodeNumber)`\n")
        reporte.write("- `(SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)`\n")
        reporte.write("- `(SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)`\n\n")
        reporte.write("Where normalized means: trimmed, collapsed spaces, and lowercased for comparison.\n\n")
        reporte.write("When duplicates were found, the best record was selected using this priority:\n\n")
        reporte.write("1. Episodes with valid AirDate over 'Unknown'\n")
        reporte.write("2. Episodes with a known title over 'Untitled Episode'\n")
        reporte.write("3. Episodes with valid Season and Episode numbers\n")
        reporte.write("4. If still tied, the first entry encountered was kept\n")