import sys
import re
from collections import Counter

def analizar_frecuencias(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    texto = texto.lower()

    texto_limpio = re.sub(r'[^\w\s]', '', texto)

    palabras = texto_limpio.split()

    if not palabras:
        print("El archivo está vacío o no contiene palabras válidas.")
        return

    contador = Counter(palabras)

    top_10 = contador.most_common(10)

    print("\n--- Top 10 palabras más frecuentes ---")
    print(f"{'Palabra':<20} | Frecuencia")
    print("-" * 35)
    for palabra, frecuencia in top_10:
        print(f"{palabra:<20} | {frecuencia}")
    print("-" * 35)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python freq.py <ruta_al_archivo.txt>")
    else:
        analizar_frecuencias(sys.argv[1])
