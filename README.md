# Proofpoint Technical Challenge

This repository contains the solutions for the Technical Challenge.

## Part B: The Streaming Service’s Lost Episodes

This script processes a corrupted episode catalog in CSV format, validates constraints, and writes out a clean dataset and quality report.

### Features
- Parses and normalizes raw input from CSV.
- Fixes missing and invalid fields using safe defaults.
- Detects and removes duplicate episodes based on priority rules (Air Date > Episode Title > Valid Numbers).
- Generates a cleaned catalog (`output/episodes_clean.csv`) sorted by series and seasons.
- Generates a data quality report (`output/report.md`) with counts and the deduplication strategy.

### How to run

```bash
python3 src/main.py
```
*(Requires `input/episodes.csv` to be present)*

---

## Part C: Word Frequency Analysis

This script reads a text file and performs a word frequency analysis, ignoring case and punctuation.

### Features
- Removes punctuation natively without affecting accented characters.
- Converts everything to lowercase.
- Counts words and outputs a formatted table of the **top 10 most frequent words**.

### How to run

```bash
python3 src/freq.py <path_to_txt_file>
```

**Example:**
```bash
python3 src/freq.py input/test_texto.txt
```