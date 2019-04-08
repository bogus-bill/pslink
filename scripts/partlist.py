import sys

import csv
import xlrd


def main():
    args = sys.argv
    if len(args) < 2:
        print("No Excel file given")
        return

    parts = []
    part_ids = set()

    wb = xlrd.open_workbook(args[1])
    for sheet_name in wb.sheet_names():
        sheet = wb.sheet_by_name(sheet_name)
        for r in range(1, sheet.nrows):
            part_number = _cell_str(sheet, r, 1).upper()
            if part_number == "":
                break
            if part_number in part_ids:
                continue
            part_ids.add(part_number)
            part_name = _cell_str(sheet, r, 4)
            parts.append((part_number, part_name))

    parts.sort(key=lambda x: x[0])
    with open(args[1] + "_parts.csv", "w", encoding="utf-8", newline="\n") as f:
        writer = csv.writer(f)
        for part in parts:
            writer.writerow([part[0], part[1], ""])

def _cell_str(sheet, row, col) -> str:
    cell = sheet.cell(row, col)
    if cell is None:
        return ""
    if cell.value is None:
        return ""
    return str(cell.value).strip()


if __name__ == "__main__":
    main()
