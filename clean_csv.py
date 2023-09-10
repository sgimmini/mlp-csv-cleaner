"""
Python script to clean a badly formatted CSV file, that is exported by the bank.
"""

import argparse
import csv
import chardet


def read_badly_formatted_csv(filename: str,
                             remove_header: bool = False,
                             remove_footer: bool = False) -> list:
    """
    Read a badly formatted CSV file, that is exported by the bank.
    Return a list of lines.
    Optionally remove the header and footer of the CSV file to have a clean CSV file.
    """

    def detect_encoding(file_path: str) -> str:
        """
        Return the encoding of a file.
        """
        with open(file_path, 'rb') as f:
            return chardet.detect(f.read())['encoding']

    encoding = detect_encoding(filename)

    with open(filename, 'r', encoding=encoding) as f:
        lines = f.readlines()

    cleaned_lines = []
    buffer = ""
    for line in lines:
        buffer += line.strip()
        # complete the buffer when it has a balanced number of quotes
        if buffer.count('"') % 2 == 0:
            cleaned_lines.append(buffer)
            buffer = ""

    # header contains useless information; can be removed
    if remove_header:
        # find the index of the line that starts with "Buchungstag"
        for i, line in enumerate(cleaned_lines):
            # the header is always up until the line that starts with "Buchungstag"
            if line.startswith('"Buchungstag"'):
                cleaned_lines = cleaned_lines[i:]
                break

    # footer contians useless information; can be removed
    if remove_footer:
        cleaned_lines = cleaned_lines[:-3]

    return cleaned_lines


def save_cleaned_csv(lines: list,
                     output_filename: str = "cleaned.csv") -> None:
    """
    Save the cleaned CSV file. 
    Takes a list of lines as input. 
    """
    with open(output_filename, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        for line in lines:
            rows = list(csv.reader([line], delimiter=';', quotechar='"'))
            for row in rows:
                writer.writerow(row)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Clean a badly formatted CSV file.')
    parser.add_argument('filename', type=str,
                        help='the filename of the CSV file to clean')
    parser.add_argument('--remove-header', action='store_true',
                        help='remove the header of the CSV file')
    parser.add_argument('--remove-footer', action='store_true',
                        help='remove the footer of the CSV file')
    args = parser.parse_args()

    save_cleaned_csv(
        read_badly_formatted_csv(filename=args.filename,
                                 remove_header=args.remove_header,
                                 remove_footer=args.remove_footer),
        args.filename.replace(".csv", "_cleaned.csv"))

    print(f"Cleaned CSV saved to {args.filename.replace('.csv', '_cleaned.csv')}")
