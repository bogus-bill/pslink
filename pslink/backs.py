import csv


class ProductInfo(object):
    """Instances of this class describe a product in a background database."""

    def __init__(self):
        self.process_uuid = ''
        self.process_name = ''
        self.product_uuid = ''
        self.product_name = ''
        self.product_unit = ''


def read_products(fpath: str) -> list:
    """Read the list of product information from the given file. """
    infos = []
    with open(fpath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            pinfo = ProductInfo()
            pinfo.process_uuid = row[0]
            pinfo.process_name = row[1]
            pinfo.product_uuid = row[2]
            pinfo.product_name = row[3]
            pinfo.product_unit = row[4]
            infos.append(pinfo)
    return infos
