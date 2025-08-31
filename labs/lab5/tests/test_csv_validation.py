import csv
from pathlib import Path
from csv_checks import REQUIRED_COLUMNS, load_rows, check_required_columns, validate_rows
DATA=Path('data/people.csv')

def test_csv_header_columns():
    with DATA.open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        assert check_required_columns(reader.fieldnames)

def test_csv_rows_valid():
    rows=load_rows(DATA)
    assert validate_rows(rows)
