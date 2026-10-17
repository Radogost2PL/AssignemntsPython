import csv
from pathlib import Path

from download_app import exceptions

import logging

logging.basicConfig(level=logging.DEBUG)

MISSING = "-"

class SimpleETL:

    def __init__(self, input_path, output_dir=None, delimiter=","):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir) if output_dir else self.input_path.parent
        self.delimiter = delimiter

    def extract(self):
        try:
            with open(self.input_path, newline="", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    logging.debug(f"Przetwarzanie lini: {line}")
                    if line:
                        yield [cell.strip() for cell in line.split(self.delimiter)]
        except (OSError, UnicodeDecodeError) as e:
            raise exceptions.ProcessingError(
                f"Nie można odczytać pliku {self.input_path}: {e}"
            ) from e

    def transform(self, rows):
        """Zwraca generator wyników dla wierszy, których kolumna 0 jest liczbą."""
        """Sprawdza czy lista zaczyna się od indeksu liczby całkowitej."""
        data_rows = (row for row in rows if row[0].lstrip("-").isdigit())
        return (self._process_row(row) for row in data_rows)

    def _process_row(self, row):
        number = int(row[0])
        cells = row[1:]
        try:
            values = [float(c) for c in cells if c != MISSING]
        except ValueError as e:
            raise exceptions.DataFormatError(
                f"Niepoprawna wartość w wierszu {number}: {e}"
            ) from e

        """Zapisanie pozycji brakujących danych. Liczenie od 1 zamiast zera."""
        missing = [column_number for column_number, cell in enumerate(cells, start=1) if cell == MISSING]
        total = sum(values)
        mean = total / len(values) if values else None
        logging.debug(f"Obliczone wartośći: row: {row}, number: {number}, total: {total}, mean: {mean}, missing: {missing}")
        return number, total, mean, missing

    def load(self, records):
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            values_path = self.output_dir / "values.csv"
            missing_path = self.output_dir / "missing_values.csv"

            with open(values_path, "w", newline="", encoding="utf-8") as vf, \
                    open(missing_path, "w", newline="", encoding="utf-8") as mf:
                values_writer = csv.writer(vf)
                missing_writer = csv.writer(mf)
                values_writer.writerow(["numer", "suma", "srednia"])
                missing_writer.writerow(["numer", "indeksy_brakujacych"])

                for number, total, mean, missing in records:
                    values_writer.writerow(
                        [number, total, "" if mean is None else round(mean, 4)]
                    )
                    missing_writer.writerow([number, " ".join(map(str, missing))])
        except OSError as e:
            raise exceptions.ProcessingError(f"Nie można zapisać wyników: {e}") from e

        return values_path, missing_path

    def run(self):
        logging.info("PRZETWARZANIE PLIKU")
        return self.load(self.transform(self.extract()))