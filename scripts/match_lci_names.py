import csv

import pslink.symap as symap
import pslink.semap as semap


def main():
    g = semap.read_file('../products.semapl')
    matches = []
    with open('../data/link_products.txt', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            name = row[3]
            match = g.find_node(name, symap.words_equality)
            if match != ():
                matches.append((match[0], match[1], name))
    matches.sort(key=lambda x: -x[0])
    for m in matches:
        print(m)


if __name__ == '__main__':
    main()
