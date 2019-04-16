import csv

import pslink.semap as semap
import pslink.partatts as partatts


def main():
    product_infos = []
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
            product_infos.append(pinfo)

    g = semap.read_file('../products.semapl')
    print(len(g.nodes))
    g.link_products(product_infos)
    print(len(g.nodes))

    materials = partatts.from_file("../densities.txt").keys()
    for material in materials:
        print(material)
        if material != "steel":
            continue
        products = g.find_products(material)
        for product in products:  # type: semap.ProductInfo
            print("  -> ", product.product_name)


if __name__ == '__main__':
    main()
