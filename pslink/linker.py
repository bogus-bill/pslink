import csv
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
        self.g = None  # type: Optional[semap.Graph]

        # categories
        self.root_part_category = None  # type: Optional[olca.Category]
        self.used_part_category = None  # type: Optional[olca.Category]
        self.component_category = None  # type: Optional[olca.Category]
        self.material_category = None  # type: Optional[olca.Category]

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
        log.info("created graph with {} nodes and {} edges",
                 len(self.g.nodes), len(self.g.edges))
        gpath = os.path.join(self.data_dir, fname + "_graph.semapl")
        semap.write_file(self.g, gpath)
        log.info("dumped graph with linked products to %s", gpath)

        # initialize the pack writer
        fpath = os.path.join(self.data_dir, fname)
        if os.path.exists(fpath):
            log.warning("File %s already exists and will be overwritten", fpath)
            os.remove(fpath)
        self.writer = olca.pack.Writer(fpath)
        self.__init_write_categories()

    def __init_write_categories(self):
        log.info("write categories")
        root = olca.Category()
        root.name = "Root components"
        root.id = str(uuid.uuid4())
        root.model_type = olca.ModelType.PROCESS
        self.writer.write(root)
        self.root_part_category = root

        used = olca.Category()
        used.name = "Used components"
        used.id = str(uuid.uuid4())
        used.model_type = olca.ModelType.PROCESS
        self.writer.write(used)
        self.used_part_category = used

        components = olca.Category()
        components.name = "Components"
        components.id = str(uuid.uuid4())
        components.model_type = olca.ModelType.FLOW
        self.writer.write(components)
        self.component_category = components

        materials = olca.Category()
        materials.name = "Materials"
        materials.id = str(uuid.uuid4())
        materials.model_type = olca.ModelType.FLOW
        self.writer.write(materials)
        self.material_category = materials
