import pslink.semap as semap
import pslink.backs as backs


def main():
    g = semap.read_file('../data/product_net.semapl')
    product_infos = backs.read_products("../data/background_products.txt")
    print("syntactic mapping of %i background products" % len(product_infos))
    g.link_products(product_infos)

    g.explain("rubber fluorocarbon class fpm")


if __name__ == "__main__":
    main()
