# test our string similarity method with the UNSPSC codes and the product
# names from the LCA commons

import csv
import pslink.symap as symap


def main():
    commons_names = []
    with open("../data/lca_commons_product_names.txt", "r",
              encoding='utf-8') as f:
        text = f.read()
        for line in text.splitlines():
            words = symap.keywords(line, strip_lci_terms=True)
            if len(words) == 0:
                continue
            commons_names.append((line, words))

    un_codes = []
    with open("../data/unspsc_codes.txt", "r", encoding="utf-8") as f:
        text = f.read()
        for line in text.splitlines():
            if line.strip() == "":
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            code = parts[0].strip()
            words = symap.keywords(parts[1])
            if len(words) == 0:
                continue
            un_codes.append((code, parts[1], words))

    matches = []
    for commons_name in commons_names:
        match = None
        score = 0.0
        for un_code in un_codes:
            s = symap.words_equality(
                commons_name[1], un_code[2])
            if match is None or s > score:
                match = un_code
                score = s
        print(commons_name[0], " => ", match[0], match[1])

        m = [commons_name[0]]
        if score == 0.0:
            m.extend(["-", "-"])
        else:
            m.extend([match[0], match[1]])

    with open("../data_commons_2_unspsc.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(matches)


if __name__ == "__main__":
    main()
