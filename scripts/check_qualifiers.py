# collects the qualifiers in the names of the background products

import csv

import pslink.symap as symap


def main():
    ranking = {}
    with open('../data/background_products.txt', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            name = row[3]
            _, qualifiers = symap.qpartition(name)
            for q in qualifiers:
                rank = ranking.get(q, 0)
                ranking[q] = rank + 1
    ranking = [(r, q) for q, r in ranking.items()]
    ranking.sort(key=lambda x: x[1])
    for r in ranking:
        print("%s" % r[1])


if __name__ == '__main__':
    main()
