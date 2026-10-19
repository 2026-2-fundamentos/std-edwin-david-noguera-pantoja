#"""Convierte los datos de conductores de CSV a JSON."""

import csv
import json
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
IMPUT_FILE = PROJECT_FOLDER / "data" / "drivers.csv"
OUTPUT_FILE = PROJECT_FOLDER / "submission" / "drivers.json"
REQUIERE_COLUNS = ("driverId", "name", "certified", "wage-plan") # necesarias en el json y sea valido
SENSITIV_COLUNS = ("ssn", "location")

def read_csv_file(input_file):
    """Lee un archivo CSV y devuelve una lista de diccionarios."""
    input_file = Path(input_file)

    with input_file.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        if headers is None:
            raise ValueError("El archivo CSV debe incluir encabezados de columna.")

        if len(headers) != len(set(headers)):
            raise ValueError("Los encabezados del CSV no deben repetirse.")

        records = list(reader)

    return headers, records

def validate_requiere_colunms(headers):
    """Verifica ..."""
    missing_columns = sorted(set(REQUIERE_COLUNS)-set(headers ))

    if missing_columns:
        missing_columns = ". ".join(missing_columns)
        raise ValueError(f'faltan columnas requeridas: {missing_columns}.')

def make_safe_records(records): #Cuidar los datos sencibles
    """filtra por las columnas que se oueden y no entregar"""
    return [
        {
            column: value
            for column, value in record.items()
            if column not in SENSITIV_COLUNS
         }
         for record in records
        
    ]


def write_json_records (records, output_file):
    """Escribe una lista de diccionarios en un archivo JSON."""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)

def convert_csv_to_json(input_file, output_file):
    """valida, minimiza, y serialyza el driver data de csv a json."""
    headers, records = read_csv_file(input_file)
    validate_requiere_colunms(headers)
    safe_records = make_safe_records(records) #asegura los registros
    write_json_records(safe_records, output_file)
    return safe_records

def main():
    """Crea el clasroom JSON export el el sunmision folder"""
    convert_csv_to_json(IMPUT_FILE, OUTPUT_FILE)

if __name__ == "__main__":
    main()