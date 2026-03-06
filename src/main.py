import csv
import re
from datetime import datetime

INPUT_FILE = "input/episodes.csv"
OUTPUT_FILE = "output/episodes_clean.csv"
REPORT_FILE = "output/report.md"

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

def write_csv(records):

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "SeriesName",
                "SeasonNumber",
                "EpisodeNumber",
                "EpisodeTitle",
                "AirDate",
            ],
        )

        writer.writeheader()

        for r in records:
            writer.writerow(r)

def write_report(metrics):

    with open(REPORT_FILE, "w", encoding="utf-8") as f:

        f.write("# Data Quality Report\n\n")

        f.write(f"- Total number of input records: {metrics['input_count']}\n")
        f.write(f"- Total number of output records: {metrics['output_count']}\n")
        f.write(f"- Number of discarded entries: {metrics['discarded_count']}\n")
        f.write(f"- Number of corrected entries: {metrics['corrected_count']}\n")
        f.write(f"- Number of duplicates detected: {metrics['duplicates_count']}\n\n")
        
        f.write("## Explanation of the deduplication strategy\n")
        f.write("Episodes are considered duplicates if they refer to the same Series (normalized), Season, and Episode; ")
        f.write("or the same Series, Season, and Title (if Episode is missing); ")
        f.write("or the same Series, Episode, and Title (if Season is missing).\n\n")
        f.write("When a duplicate is found, the system keeps the \"best\" record based on the following priority:\n")
        f.write("1. Episodes with a valid Air Date over 'Unknown'\n")
        f.write("2. Episodes with a known Episode Title over 'Untitled Episode'\n")
        f.write("3. Episodes with a valid Season Number (> 0) and Episode Number (> 0)\n")
        f.write("4. If still tied, the first entry encountered in the file is kept.\n")

def is_better_record(new_rec, old_rec):
    # Rule 1
    new_has_date = (new_rec["AirDate"] != "Unknown")
    old_has_date = (old_rec["AirDate"] != "Unknown")
    if new_has_date and not old_has_date:
        return True
    if old_has_date and not new_has_date:
        return False
        
    # Rule 2
    new_has_title = (new_rec["EpisodeTitle"] != "Untitled Episode")
    old_has_title = (old_rec["EpisodeTitle"] != "Untitled Episode")
    if new_has_title and not old_has_title:
        return True
    if old_has_title and not new_has_title:
        return False
        
    # Rule 3
    new_has_numbers = (new_rec["SeasonNumber"] > 0 and new_rec["EpisodeNumber"] > 0)
    old_has_numbers = (old_rec["SeasonNumber"] > 0 and old_rec["EpisodeNumber"] > 0)
    if new_has_numbers and not old_has_numbers:
        return True
    if old_has_numbers and not new_has_numbers:
        return False
        
    # Rule 4: first entry default
    return False

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

def deduplicate(records, metrics):

    result = []
    metrics["duplicates_count"] = 0

    for rec in records:

        duplicate_index = -1

        for i, existing in enumerate(result):
            if is_duplicate(existing, rec):
                duplicate_index = i
                break

        if duplicate_index != -1:
            metrics["duplicates_count"] += 1
            if is_better_record(rec, result[duplicate_index]):
                result[duplicate_index] = rec
        else:
            result.append(rec)
            
    metrics["output_count"] = len(result)

    result.sort(key=lambda r: (r["SeriesName"].lower(), r["SeasonNumber"], r["EpisodeNumber"]))

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
        value = value.strip()
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except:
        return "Unknown"

def clean_row(fila):
    corrected = False

    while len(fila) < 5:
        fila.append("")
        corrected = True

    fila = fila[:5]

    series, season, episode, title, airdate = fila

    series_clean = normalize_text(series)
    if series != series_clean:
        corrected = True

    season_old = season
    season = parse_number(season)
    if str(season) != str(season_old).strip():
        corrected = True

    episode_old = episode
    episode = parse_number(episode)
    if str(episode) != str(episode_old).strip():
        corrected = True

    title_clean = normalize_text(title)
    if not title_clean:
        title_clean = "Untitled Episode"
        corrected = True
    elif title != title_clean:
        corrected = True

    airdate_old = airdate
    airdate = parse_date(airdate)
    if airdate != airdate_old.strip():
        if airdate == "Unknown" and airdate_old.strip() != "Unknown":
            corrected = True
        elif airdate != airdate_old.strip():
             corrected = True

    record = {
        "SeriesName": series_clean,
        "SeasonNumber": season,
        "EpisodeNumber": episode,
        "EpisodeTitle": title_clean,
        "AirDate": airdate,
    }
    return record, corrected

def read_csv(path):
    filas = []
    
    metrics = {
        "input_count": 0,
        "discarded_count": 0,
        "corrected_count": 0,
    }

    with open(path, newline='', encoding='utf-8') as archivo:
        reader = csv.reader(archivo)

        for fila in reader:
            metrics["input_count"] += 1
            record, was_corrected = clean_row(fila)

            if should_discard(record):
                metrics["discarded_count"] += 1
                continue

            if was_corrected:
                metrics["corrected_count"] += 1

            filas.append(record)

    return filas, metrics

def main():

    filas, metrics = read_csv(INPUT_FILE)

    cleaned = deduplicate(filas, metrics)

    write_csv(cleaned)

    write_report(metrics)

    print("Procesamiento finalizado")

if __name__ == "__main__":
    main()
