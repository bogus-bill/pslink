# converts the UNSPSC classification available from here
# https://catalog.data.gov/dataset/unspsc-codes to a semapl file.

import csv
import sys


def main():
    args = sys.argv
    if len(args) < 2:
        print('no file path given')
        exit(1)
        return

    g = {}
    with open(args[1], 'r', encoding='latin1') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            p1 = norm(row[1])
            p2 = norm(row[3])
            p3 = norm(row[5])
            p4 = norm(row[7])
            add_relation(g, p1, p2)
            add_relation(g, p2, p3)
            add_relation(g, p3, p4)

    with open(args[1] + '.semapl', 'w', encoding='utf-8') as f:
        for broader, n in g.items():
            f.writelines(
                ['"%s"  , "%s"^\n' % (narrower, broader) for narrower in n])


def add_relation(graph: dict, broader: str, narrower: str):
    """Adds a relation `broader -> narrower` to the given graph dictionary """
    n = graph.get(broader)
    if n is None:
        n = []
        graph[broader] = n
    if narrower in n:
        return
    n.append(narrower)


def norm(s: str) -> str:
    if s is None:
        return ''
    if not isinstance(s, str):
        s = str(s)
    return s.strip().lower()


if __name__ == '__main__':
    main()
