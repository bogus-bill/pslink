from dataclasses import asdict, dataclass
import csv


@dataclass
class ProductInfo:
    """Instances of this class describe a product in a background database."""
    process_uuid : str = ''
    process_name : str = ''
    product_uuid : str = ''
    product_name : str = ''
    product_unit : str = ''
    process_country : str = ''

    def as_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

    def print(self):
        return f"{self.product_name} - {self.score} - {self.process_name}"


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
            pinfo.process_country = row[2]
            pinfo.product_uuid = row[3]
            pinfo.product_name = row[4]
            pinfo.product_unit = row[5]
            infos.append(pinfo)
    return infos
