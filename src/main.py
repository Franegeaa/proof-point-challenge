import csv
import re
from datetime import datetime

INPUT_FILE = "input/episodes.csv"

def normalize_text(value):
    if not value:
        return ""

    value = value.strip()
    value = re.sub(r"\s+", " ", value)

    return value

def parse_number(value):
    try:
        n = int(value)
        if n < 0:
            return 0
        return n
    except:
        return 0

def parse_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except:
        return "Unknown"

def clean_row(fila):

    while len(fila) < 5:
        fila.append("")

    fila = fila[:5]

    series, season, episode, title, airdate = fila

    series = normalize_text(series)

    season = parse_number(season)
    episode = parse_number(episode)

    title = normalize_text(title)
    if not title:
        title = "Untitled Episode"

    airdate = parse_date(airdate)

    return {
        "SeriesName": series,
        "SeasonNumber": season,
        "EpisodeNumber": episode,
        "EpisodeTitle": title,
        "AirDate": airdate,
    }

def read_csv(path):
    filas = []
    
    with open(path, newline='', encoding='utf-8') as archivo:
        reader = csv.reader(archivo)

        for fila in reader:
            filas.append(clean_row(fila))

    return filas

def main():
    filas = read_csv(INPUT_FILE)

    print(f"filas procesadas: {len(filas)}")


if __name__ == "__main__":
    main()
