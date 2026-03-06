# Data Quality Report

Total input records: 44 
Total output records: 27 
Discarded entries: 2 
Corrected entries: 19 
Duplicates detected: 15 

## Deduplication Strategy

Duplicate episodes are detected using three alternative keys based on normalized fields.

Once a duplicate is detected, the script selects the best record using a scoring function called `calcular_puntaje`.
This function implements the priority rules defined in the specification by assigninga weighted score to each record.
The weights reflect the order of importance described in the problem statement.

Scoring criteria:

- Episodes with a valid AirDate receive the highest priority over those with 'Unknown'.
- Episodes with a known title are preferred over those labeled 'Untitled Episode'.
- Episodes with valid Season and Episode numbers receive additional priority.

When two duplicate records are found, their scores are compared and the record with the higher score is kept.
If both records have the same score, the first occurrence in the dataset is preserved.
