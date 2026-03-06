# Proofpoint Internship Challenge 2026

This repository contains my solution for the Proofpoint Intern Program technical challenge.
The project includes two Python exercises focused on text processing and data cleaning.


## Project Structure
```
.
├── EjercicioExtra
│   ├── Contador_Palabras.py
│   └── textoPrueba.txt
│
└── EjercicioSeries
    ├── ejercicioB.py
    ├── catalog.csv
    ├── episodes_clean.csv
    └── report.md
```
# Exercise 1 — Word Frequency Analysis

Located in **EjercicioExtra**
This program reads a text file and performs a word frequency analysis.

### Features
- Reads a text file as input
- Ignores punctuation and special characters
- Word comparison is case insensitive
- Counts how many times each word appears
- Displays the 10 most frequent words along with their frequency

### Test File
A sample file textoPrueba.txt is included in the folder to test the program and verify that the analysis works correctly.

### Output
The program prints the **top 10 most frequent words** and their occurrence count.

---

# Exercise 2 — List of Series Data Cleaning

Located in **EjercicioSeries**

This program processes a **CSV catalog of TV series episodes** and performs data validation, normalization, and deduplication.

---

## Features

The script:

- Validates numeric fields such as season and episode numbers
- Handles missing or invalid values
- Normalizes text fields (series name and episode title)
- Validates multiple date formats
- Detects and removes duplicate episodes
- Keeps the best record when duplicates exist

---

## Considerations

While implementing the script, I made several decisions to handle inconsistent and potentially messy datasets more reliably.

### CSV delimiter
The provided dataset uses `;` as a separator.
Because of this, I explicitly parse each row using this delimiter to correctly split the columns.

---

### Text normalization
To simplify comparisons when detecting duplicates, I normalize text fields such as series names and episode titles by:
- trimming leading and trailing spaces
- collapsing multiple spaces into a single space
- converting the text to lowercase

This helps ensure that small formatting differences do not prevent correct duplicate detection.

---

### Flexible date validation

I implemented validation that accepts several common formats, including:

- ISO format (`YYYY-MM-DD`)
- European format (`DD/MM/YYYY`)
- American format (`MM-DD-YYYY`)
- Alternative ISO format (`YYYY/MM/DD`)

If a date does not match any of these formats, it is treated as invalid and replaced with `"Unknown"`.

---

### Duplicate resolution

When duplicate episodes are detected, I implemented a simple scoring system to keep the most complete record.

Episodes with:
- valid dates
- proper titles
- valid season and episode numbers

are prioritized over incomplete entries.

---

## Test Dataset
The repository includes a **catalog.csv** file containing multiple examples with intentional data issues such as:

- Missing values
- Invalid dates
- Negative numbers
- Duplicate records

This allows testing that the script correctly cleans and filters invalid rows.

---

## Output Files

The program generates two files:

### episodes_clean.csv

A cleaned and normalized dataset containing the final list of valid episodes.

### report.md

A data quality report that includes:
- Total input records
- Total output records
- Number of discarded entries
- Number of corrected entries
- Number of detected duplicates

It also explains the deduplication strategy used in the cleaning process.

## How to Run

### Exercise 1

```bash
python Contador_Palabras.py
```
### Exercise 2
```
python ejercicioB.py
```
## Author

**Valentin Alberto Gallardo Scaltriti**
