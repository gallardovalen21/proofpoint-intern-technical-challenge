# Data Quality Report

Total input records: 44
Total output records: 27
Discarded entries: 2
Corrected entries: 19
Duplicates detected: 15

## Deduplication Strategy

Episodes were considered duplicates when they matched one of the following keys:

- `(SeriesName_normalized, SeasonNumber, EpisodeNumber)`
- `(SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)`
- `(SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)`

Where normalized means: trimmed, collapsed spaces, and lowercased for comparison.

When duplicates were found, the best record was selected using this priority:

1. Episodes with valid AirDate over 'Unknown'
2. Episodes with a known title over 'Untitled Episode'
3. Episodes with valid Season and Episode numbers
4. If still tied, the first entry encountered was kept
