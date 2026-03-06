import csv

INPUT_FILE = "input/episodes.csv"

def read_csv(path):
    filas = []
    
    with open(path, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)

        for fila in reader:
            filas.append(fila)
    return filas

def main():
    filas = read_csv(INPUT_FILE)

    print(f"Total filas leidas: {len(filas)}")


if __name__ == "__main__":
    main()
