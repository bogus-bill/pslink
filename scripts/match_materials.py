import glob

import olca
import pslink.symap as symap


def get_materials(fpath: str) -> list:
    materials = set()
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f.read().splitlines():
            parts = line.split(";")
            key = parts[0].strip().lower()
            if key == "material":
                mat = parts[1].strip().lower()  # type: str
                if mat.endswith("overall"):
                    mat = mat[0:len(mat) - 7].strip()
                materials.add(mat)
    return list(materials)


if __name__ == "__main__":
    materials = set()
    for fpath in glob.glob("../data/components/*.txt"):
        mats = get_materials(fpath)
        if len(mats) == 0:
            print("No materials found in", fpath)
        else:
            materials.update(mats)
    for mat in materials:
        print(mat)

    client = olca.Client(8080)
    flow_names = [f.name for f in client.get_descriptors(olca.Flow)]
    for mat in materials:
        match = symap.best_match(mat, flow_names)
        print("%s --> %s" % (mat, match))
