from functools import reduce

import pslink.symap as symap
import pslink.semap as semap
import pslink.backs as backs


def words_equality(phrase_a: str, phrase_b: str) -> float:
    def len_red(x: int, y: str):
        return x + len(y)

    a = symap.keywords(phrase_a)
    len_a = reduce(len_red, a, 0)
    b = symap.keywords(phrase_b)
    len_b = reduce(len_red, b, 0)
    n = max(len_a, len_b)
    s = 0
    for wa in a:
        if wa in b:
            s += len(wa)
            b.remove(wa)
    return s / n


def main():
    # build the product graph and link the background products
    g = semap.read_file('../data/product_net.semapl')
    product_infos = backs.read_products("../data/background_products.txt")
    g.link_products(product_infos)

    g.explain("rubber fluorocarbon class fpm", matcher=words_equality, max_level=3)


if __name__ == "__main__":
    main()
