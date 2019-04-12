# test our string similarity method with the UNSPSC codes and the product
# names from the LCA commons

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

    i = 0
    for commons_name in commons_names[10:]:
        match = None
        score = 0.0
        for un_code in un_codes:
            s = symap.words_similarity(
                commons_name[1], un_code[2])
            if match is None or s > score:
                match = un_code
                score = s
        print(commons_name[0], " => ", match[0], match[1])
        i += 1
        if i == 100:
            break


if __name__ == "__main__":
    main()
