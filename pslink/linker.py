import glob
import logging as log
import os
import uuid

import olca
import olca.pack
import xlrd

import pslink.backs as backs
import pslink.semap as semap
import pslink.partatts as partatts

from typing import Optional


class Linker(object):

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.densities = {}
        self.created_processes = {}
        self.created_products = {}
        self.created_materials = {}

        self.g = None  # type: Optional[semap.Graph]
        self.matched_products = {}

        # categories
        self.root_part_category = None  # type: Optional[olca.Ref]
        self.used_part_category = None  # type: Optional[olca.Ref]
        self.component_category = None  # type: Optional[olca.Ref]
        self.material_category = None  # type: Optional[olca.Ref]

        self.writer = None  # type: Optional[olca.pack.Writer]

    def run(self):

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
        background_products = backs.read_products(bpath)
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
        gpath = os.path.join(self.data_dir, "out", "linked_graph.semapl")
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
        fpath = os.path.join(self.data_dir, "out", "generated_jsonld.zip")
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
        for product in self.created_products.values():
            self.writer.write(product)
        for process in self.created_processes.values():
            self.writer.write(process)
        for material in self.created_materials.values():
            self.writer.write(material)
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
                uid = part_id(part_number)
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
                    puid = part_id(parent_number)
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
                    inp.flow = olca.ref(olca.Flow, product.id)
                    inp.default_provider = olca.ref(
                        olca.Process, "proc_" + product.id)
                    parent.exchanges.append(inp)

    def __create_product(self, number: str, name: str) -> olca.Flow:
        flow = olca.Flow()
        if name == "":
            flow.name = number
        else:
            flow.name = "%s - %s" % (number, name)
        log.info("create product %s", flow.name)
        flow.id = part_id(number)
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
        exchange.flow = olca.ref(olca.Flow, product.id)
        exchange.quantitative_reference = True
        process.exchanges = [exchange]
        return process

    def __infer_inputs(self, part_number: str, process: olca.Process):
        part_file = self.data_dir + "/components/%s.txt" % part_id(part_number)
        if not os.path.isfile(part_file):
            log.info("no part data for %s", part_number)
            return
        part_atts = partatts.from_file(part_file)
        inputs = partatts.material_inputs(part_atts, self.densities)
        if len(inputs) == 0:
            log.info("could not extract materials from file %s", part_file)
            return
        for inp in inputs:
            mat_name = inp[0]  # type: str
            flow, matches = self.__get_material(mat_name)
            if len(matches) == 0:
                e = olca.Exchange()
                e.amount = inp[1]
                e.input = True
                e.flow = olca.ref(olca.Flow, flow.id)
                process.exchanges.append(e)
            else:
                for match in matches:  # type: backs.ProductInfo
                    e = olca.Exchange()
                    e.amount = inp[1] / len(matches)
                    e.input = True
                    e.flow = olca.ref(
                        olca.Flow, match.product_uuid)
                    e.default_provider = olca.ref(
                        olca.Process, match.process_uuid)
                    process.exchanges.append(e)

    def __get_material(self, name: str):
        uid = str(uuid.uuid3(uuid.NAMESPACE_OID,
                             "material/" + name.strip().lower()))
        flow = self.created_materials.get(uid)
        if flow is not None:
            return flow, self.matched_products[uid]

        log.info("new material %s found; search for background links", name)
        matches = self.g.find_products(name)
        log.info("found %i possible matches", len(matches))
        self.matched_products[uid] = matches

        flow = olca.Flow()
        flow.name = name
        flow.id = uid
        flow.flow_type = olca.FlowType.PRODUCT_FLOW
        flow.category = self.material_category

        # set mass as flow property
        fp = olca.FlowPropertyFactor()
        fp.conversion_factor = 1.0
        fp.reference_flow_property = True
        fp.flow_property = olca.ref(
            olca.FlowProperty, "93a60a56-a3c8-11da-a746-0800200b9a66")
        flow.flow_properties = [fp]
        self.created_materials[uid] = flow
        return flow, matches


def _cell_str(sheet, row, col) -> str:
    cell = sheet.cell(row, col)
    if cell is None:
        return ""
    if cell.value is None:
        return ""
    return str(cell.value).strip()


def part_id(part_number: str):
    return part_number.strip().replace("/", "_")
