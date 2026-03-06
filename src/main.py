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

def normalize_compare(value):
    value = value.lower()
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    return value

def is_duplicate(a, b):

    same_series = normalize_compare(a["SeriesName"]) == normalize_compare(
        b["SeriesName"]
    )

    rule1 = (
        same_series
        and a["SeasonNumber"] == b["SeasonNumber"]
        and a["EpisodeNumber"] == b["EpisodeNumber"]
    )

    rule2 = (
        same_series
        and a["EpisodeNumber"] == b["EpisodeNumber"]
        and normalize_compare(a["EpisodeTitle"])
        == normalize_compare(b["EpisodeTitle"])
        and (a["SeasonNumber"] == 0 or b["SeasonNumber"] == 0)
    )

    rule3 = (
        same_series
        and a["SeasonNumber"] == b["SeasonNumber"]
        and normalize_compare(a["EpisodeTitle"])
        == normalize_compare(b["EpisodeTitle"])
        and (a["EpisodeNumber"] == 0 or b["EpisodeNumber"] == 0)
    )

    return rule1 or rule2 or rule3

def deduplicate(records):

    result = []

    for rec in records:

        duplicate_found = False

        for i, existing in enumerate(result):

            if is_duplicate(existing, rec):
                duplicate_found = True
                break

        if not duplicate_found:
            result.append(rec)

    return result

def should_discard(record):

    if record["SeriesName"] == "":
        return True

    episode_missing = record["EpisodeNumber"] == 0
    title_missing = record["EpisodeTitle"] == "Untitled Episode"
    airdate_missing = record["AirDate"] == "Unknown"

    if episode_missing and title_missing and airdate_missing:
        return True

    return False

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
            record = clean_row(fila)

            if should_discard(record):
                continue

            filas.append(record)

    return filas

def main():
    filas = read_csv(INPUT_FILE)

    print(f"Filas antes de deduplicar: {len(filas)}")

    deduplicated = deduplicate(filas)

    print(f"Filas despues de deduplicar: {len(deduplicated)}")

if __name__ == "__main__":
    main()
