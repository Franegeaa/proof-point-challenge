# Data Quality Report

- Total number of input records: 30
- Total number of output records: 20
- Number of discarded entries: 3
- Number of corrected entries: 20
- Number of duplicates detected: 7

## Explanation of the deduplication strategy
Episodes are considered duplicates if they refer to the same Series (normalized), Season, and Episode; or the same Series, Season, and Title (if Episode is missing); or the same Series, Episode, and Title (if Season is missing).

When a duplicate is found, the system keeps the "best" record based on the following priority:
1. Episodes with a valid Air Date over 'Unknown'
2. Episodes with a known Episode Title over 'Untitled Episode'
3. Episodes with a valid Season Number (> 0) and Episode Number (> 0)
4. If still tied, the first entry encountered in the file is kept.
