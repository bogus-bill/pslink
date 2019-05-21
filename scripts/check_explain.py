# the explain function prints out the traversal tree and
# product mapping scores for a given product name.

import pslink.symap as symap
import pslink.semap as semap
import pslink.backs as backs


def main():
    # build the product graph and link the background products
    g = semap.read_file('../data/product_net.semapl')
    product_infos = backs.read_products("../data/background_products.txt")
    g.link_products(product_infos)

    symap.add_stopword("class")
    g.explain("rubber fluorocarbon class fpm")


if __name__ == "__main__":
    main()
