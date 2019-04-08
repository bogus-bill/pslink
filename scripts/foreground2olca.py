import sys

import olca
import olca.pack
import xlrd


def main():
    args = sys.argv
    if len(args) < 2:
        print("No Excel file given")
        return

    print("Try to read data from", sys.argv[1])
    wb = xlrd.open_workbook(args[1])

    products = {}
    processes = {}

    for sheet_name in wb.sheet_names():
        sheet = wb.sheet_by_name(sheet_name)
        for r in range(1, sheet.nrows):
            part_number = _cell_str(sheet, r, 1)
            if part_number == "":
                break
            uid = part_number.lower()
            part_name = _cell_str(sheet, r, 4)
            product = products.get(uid)
            if product is None:
                product = create_product(part_number, part_name)
                products[uid] = product
                process = create_process(part_number, part_name, product)
                processes[uid] = process
            parent_number = _cell_str(sheet, r, 5)
            if parent_number != "":
                parent = processes.get(parent_number.lower())
                if parent is None:
                    print("Unknown parent: %s -> %s" % (
                          part_number, parent_number))
                    continue
                add_input(parent, product)

    w = olca.pack.Writer(sys.argv[1] + "_olca_jsonld.zip")
    for product in products.values():
        w.write(product)
    for process in processes.values():
        w.write(process)
    w.close()


def _cell_str(sheet, row, col) -> str:
    cell = sheet.cell(row, col)
    if cell is None:
        return ""
    if cell.value is None:
        return ""
    return str(cell.value).strip()


def create_product(number: str, name: str) -> olca.Flow:
    flow = olca.Flow()
    if name == "":
        flow.name = number
    else:
        flow.name = "%s - %s" % (number, name)
    flow.id = number.lower()
    flow.flow_type = olca.FlowType.PRODUCT_FLOW
    fp = olca.FlowPropertyFactor()
    fp.conversion_factor = 1.0
    fp.reference_flow_property = True
    fp.flow_property = olca.ref(
        olca.FlowProperty, "01846770-4cfe-4a25-8ad9-919d8d378345")
    flow.flow_properties = [fp]
    return flow


def create_process(number: str, name: str, product: olca.Flow) -> olca.Process:
    process = olca.Process()
    if name == "":
        process.name = number
    else:
        process.name = "%s - %s" % (number, name)
    process.id = "p::" + number.lower()
    process.process_type = olca.ProcessType.UNIT_PROCESS
    exchange = olca.Exchange()
    exchange.amount = 1.0
    exchange.input = False
    exchange.flow = product
    exchange.quantitative_reference = True
    process.exchanges = [exchange]
    return process


def add_input(process: olca.Process, product: olca.Flow):
    e = olca.Exchange()
    e.amount = 1.0
    e.input = True
    e.flow = product
    process.exchanges.append(e)


if __name__ == "__main__":
    main()
