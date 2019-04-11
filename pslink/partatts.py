"""
This module containts functions for extracting attributes of component parts.
"""


def from_file(fpath: str, encoding="utf-8") -> dict:
    """ Read the attributes of a component part from the given file. We
        assume that the attributes are stored in a simple text file where
        each line contains a key-value pair separated by a semicolon. """
    atts = {}
    with open(fpath, "r", encoding=encoding) as f:
        for line in f.read().splitlines():
            s = line.strip()
            if s == "":
                continue
            parts = line.split(";")
            if len(parts) < 2:
                continue
            atts[parts[0].strip()] = parts[1].strip()
    return atts


def materials(atts: dict) -> set:
    """ Returns a list of material names from the given attributes. """
    mat_atts = {"material", "iii material", "body material", "stem material",
                "seat material", "flow control device material",
                "spring material", "screw material"}
    suffixes = ["overall", "inner layer", "outer race member"]
    s = set()
    for k, v in atts.items():
        if not k.strip().lower() in mat_atts:
            continue
        mats = v.split(" or ")
        for m in mats:
            mat = m.strip().lower()  # type: str
            for suffix in suffixes:
                if mat.endswith(suffix):
                    mat = mat[0:len(mat) - len(suffix)].strip()
                    break
            s.add(mat)
    return s
