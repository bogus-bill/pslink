# check the consistency of the Excel files with the component trees: compare
# the tree structure which results from the level column with the parent
# pointers (there were inconsistencies in some sheets)

import glob
import xlrd


def main():
    file_count = 0
    sheet_count = 0
    error_count = 0

    for f in glob.glob("../data/*.xlsx"):
        file_count += 1
        print("check component trees in", f)
        wb = xlrd.open_workbook(f)
        for sheet_name in wb.sheet_names():
            sheet_count += 1
            print("  check sheet", sheet_name)
            sheet = wb.sheet_by_name(sheet_name)

            stack = []
            for r in range(1, sheet.nrows):
                part_number = _cell_str(sheet, r, 1)
                if part_number == "":
                    break

                level = int(sheet.cell_value(r, 0))
                while len(stack) > level:
                    stack.pop()

                if level > 0:
                    parent = _cell_str(sheet, r, 5)
                    if stack[level - 1] != parent:
                        error_count += 1
                        print("    err: row %i next=%s but parent=%s" % (
                            r, parent, stack[level - 1]))
                stack.append(part_number)

    print("scanned materials in %i files with %i sheets: found %i errors" %
          (file_count, sheet_count, error_count))


def _cell_str(sheet, row, col) -> str:
    cell = sheet.cell(row, col)
    if cell is None:
        return ""
    if cell.value is None:
        return ""
    return str(cell.value).strip()


if __name__ == "__main__":
    main()
