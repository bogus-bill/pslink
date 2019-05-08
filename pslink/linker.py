import csv
import logging as log
import os

import olca
import olca.pack
import xlrd

import pslink.semap as semap
import pslink.partatts as partatts


class Linker(object):

    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def run(self, fname="out.zip"):

        # read the material densities
        dpath = os.path.join(self.data_dir, "densities.txt")
        if not os.path.exists(dpath):
            log.error("could not find material densities: %s", dpath)
            return
        log.info("read densities from %s", dpath)
        densities = {}
        for mat, dens in partatts.from_file(dpath).items():
            densities[mat.lower().strip()] = float(dens.strip())
        log.info("found %i material densities" % len(densities))

        # read the background products
        bpath = os.path.join(self.data_dir, "background_products.txt")
        if not os.path.exists(bpath):
            log.error("could not find background products: %s", bpath)
            return
        log.info("read background products from %s", bpath)
        background_products = []
        with open('../data/link_products.txt', 'r', encoding='utf-8') as f:
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

        fpath = os.path.join(self.data_dir, fname)
        if os.path.exists(fpath):
            log.warning("File %s already exists and will be overwritten", fpath)
            os.remove(fpath)

        pw = olca.pack.Writer(fpath)
