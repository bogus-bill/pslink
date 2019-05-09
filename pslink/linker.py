import csv
import glob
import logging as log
import os
import uuid

import olca
import olca.pack
import xlrd

import pslink.semap as semap
import pslink.partatts as partatts

from typing import Optional


class Linker(object):

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.densities = {}
        self.created_products = {}
        self.created_processes = {}
        self.g = None  # type: Optional[semap.Graph]

        # categories
        self.root_part_category = None  # type: Optional[olca.Ref]
        self.used_part_category = None  # type: Optional[olca.Ref]
        self.component_category = None  # type: Optional[olca.Ref]
        self.material_category = None  # type: Optional[olca.Ref]

        self.writer = None  # type: Optional[olca.pack.Writer]

    def run(self, fname="out.zip"):

        # read the material densities
        dpath = os.path.join(self.data_dir, "densities.txt")
        if not os.path.exists(dpath):
            log.error("could not find material densities: %s", dpath)
            return
        log.info("read densities from %s", dpath)
        for mat, dens in partatts.from_file(dpath).items():
            self.densities[mat.lower().strip()] = float(dens.strip())
        log.info("found %i material densities" % len(self.densities))

        # read the background products
        bpath = os.path.join(self.data_dir, "background_products.txt")
        if not os.path.exists(bpath):
            log.error("could not find background products: %s", bpath)
            return
        log.info("read background products from %s", bpath)
        background_products = []
        with open(bpath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader)
            for row in reader:
                pinfo = semap.ProductInfo()
                pinfo.process_uuid = row[0]
                pinfo.process_name = row[1]
                pinfo.product_uuid = row[2]
                pinfo.product_name = row[3]
                pinfo.product_unit = row[4]
                background_products.append(pinfo)
        log.info("found %s background products", len(background_products))

        # read the graph
        gpath = os.path.join(self.data_dir, "product_net.semapl")
        if not os.path.exists(gpath):
            log.error("could not find product graph: %s", gpath)
            return
        log.info("read product graph from %s", gpath)
        self.g = semap.read_file(gpath)
        self.g.link_products(background_products)
        log.info("created graph with %i nodes and %i edges",
                 len(self.g.nodes), len(self.g.edges))
        gpath = os.path.join(self.data_dir, fname + "_graph.semapl")
        semap.write_file(self.g, gpath)
        log.info("dumped graph with linked products to %s", gpath)

        # collect the XLSX files from the data folder
        xpath = self.data_dir
        if not xpath.endswith("/") and not xpath.endswith("\\"):
            xpath += "/"
        xpath += "*.xlsx"
        xlsx_files = glob.glob(xpath)
        if len(xlsx_files) == 0:
            log.error("no xlsx files found in %s", self.data_dir)
            return
        log.info("found %i xlsx files", len(xlsx_files))

        # initialize the pack writer
        fpath = os.path.join(self.data_dir, fname)
        if os.path.exists(fpath):
            log.warning("file %s already exists and will be overwritten", fpath)
            os.remove(fpath)
        self.writer = olca.pack.Writer(fpath)
        self.__init_write_categories()

        for xlsx in xlsx_files:
            self.__parse_xlsx(xlsx)
        self.__write_data()

    def __init_write_categories(self):
        log.info("write categories")
        root = olca.Category()
        root.name = "Root components"
        root.id = str(uuid.uuid4())
        root.model_type = olca.ModelType.PROCESS
        self.writer.write(root)
        self.root_part_category = olca.ref(olca.Category, root.id)

        used = olca.Category()
        used.name = "Used components"
        used.id = str(uuid.uuid4())
        used.model_type = olca.ModelType.PROCESS
        self.writer.write(used)
        self.used_part_category = olca.ref(olca.Category, used.id)

        components = olca.Category()
        components.name = "Components"
        components.id = str(uuid.uuid4())
        components.model_type = olca.ModelType.FLOW
        self.writer.write(components)
        self.component_category = olca.ref(olca.Category, components.id)

        materials = olca.Category()
        materials.name = "Materials"
        materials.id = str(uuid.uuid4())
        materials.model_type = olca.ModelType.FLOW
        self.writer.write(materials)
        self.material_category = olca.ref(olca.Category, materials.id)

    def __write_data(self):
        log.info("write generated data")
        for product in self.created_products:
            self.writer.write(product)
        for process in self.created_processes:
            self.writer.write(process)
        # TODO: write created materials
        self.writer.close()

    def __parse_xlsx(self, xpath: str):
        log.info("parse XLSX file %s", xpath)
        wb = xlrd.open_workbook(xpath)
        for sheet_name in wb.sheet_names():
            log.info("parse sheet %s", sheet_name)
            sheet = wb.sheet_by_name(sheet_name)
            for r in range(1, sheet.nrows):
                part_number = _cell_str(sheet, r, 1)
                if part_number == "":
                    break
                uid = part_number.lower()
                part_name = _cell_str(sheet, r, 4)
                parent_number = _cell_str(sheet, r, 5)
                product = self.created_products.get(uid)

                # create product and process
                if product is None:
                    product = self.__create_product(part_number, part_name)
                    self.created_products[uid] = product
                    process = self.__create_process(product,
                                                    root=parent_number == "")
                    self.__infer_inputs(part_number, process)
                    self.created_processes[uid] = process

                # create input in parent component
                if parent_number != "":
                    puid = parent_number.lower()
                    parent = self.created_processes.get(puid)
                    if parent is None:
                        log.warning("Unknown parent link: %s => %s",
                                    part_number, parent_number)
                        continue
                    inp = olca.Exchange()
                    inp.amount = 1.0
                    try:
                        inp.amount = float(_cell_str(sheet, r, 3))
                    except ValueError:
                        log.warning("not a numeric quantity," +
                                    "default to 1.0; sheet=%s, row=%i",
                                    sheet_name, r)
                    inp.input = True
                    inp.flow = product
                    parent.exchanges.append(inp)

    def __create_product(self, number: str, name: str) -> olca.Flow:
        flow = olca.Flow()
        if name == "":
            flow.name = number
        else:
            flow.name = "%s - %s" % (number, name)
        log.info("create product %s", flow.name)
        flow.id = number.lower()
        flow.flow_type = olca.FlowType.PRODUCT_FLOW
        flow.category = self.component_category
        # set "number of items as the reference flow property
        fp = olca.FlowPropertyFactor()
        fp.conversion_factor = 1.0
        fp.reference_flow_property = True
        fp.flow_property = olca.ref(
            olca.FlowProperty, "01846770-4cfe-4a25-8ad9-919d8d378345")
        flow.flow_properties = [fp]
        return flow

    def __create_process(self, product: olca.Flow, root=False) -> olca.Process:
        log.info("create process %s", product.name)
        process = olca.Process()
        process.name = product.name
        process.id = "proc_" + product.id
        process.process_type = olca.ProcessType.UNIT_PROCESS
        if root:
            process.category = self.root_part_category
        else:
            process.category = self.used_part_category
        exchange = olca.Exchange()
        exchange.amount = 1.0
        exchange.input = False
        exchange.flow = product
        exchange.quantitative_reference = True
        process.exchanges = [exchange]
        return process

    def __infer_inputs(self, part_number: str, process: olca.Process):
        pass


def _cell_str(sheet, row, col) -> str:
    cell = sheet.cell(row, col)
    if cell is None:
        return ""
    if cell.value is None:
        return ""
    return str(cell.value).strip()
