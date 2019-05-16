# checks the product linking (syntactic mapping) of products from the
# background system to the product graph

import pslink.semap as semap
import pslink.backs as backs
import pslink.partatts as partatts


def main():
    # read the graph
    g = semap.read_file('../data/product_net.semapl')
    print("created graph with %i nodes and %i edges" %
          (len(g.nodes), len(g.edges)))

    # read and link products from brackground database
    product_infos = backs.read_products("../data/background_products.txt")
    print("syntactic mapping of %i background products" % len(product_infos))
    g.link_products(product_infos)
    semap.write_file(g, "../data/out/check_product_linking.semapl")
    print("dumped mapped graph to ../data/out/check_product_linking.semapl")

    # link materials
    print("link materials from foreground system ...")
    materials = partatts.from_file("../data/densities.txt").keys()
    for material in materials:
        print("\n", material)
        products = g.find_products(material)
        for product in products:  # type: backs.ProductInfo
            print("  -> ", product.product_name)


if __name__ == "__main__":
    main()
