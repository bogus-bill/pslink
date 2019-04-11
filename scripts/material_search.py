import glob

import pslink.partatts as partatts

if __name__ == "__main__":

    mat_atts = {"material", "iii material", "body material", "stem material",
                "seat material", "flow control device material",
                "spring material", "screw material"}

    known_materials = partatts.from_file("../densities.txt").keys()

    new_keys = {}
    new_materials = set()
    for fpath in glob.glob("../data/components/*.txt"):
        atts = partatts.from_file(fpath)
        for mat in partatts.materials(atts):
            if mat not in known_materials:
                new_materials.add(mat)
        for akey in atts.keys():
            k = akey.strip().lower()
            if "material" in k and k not in mat_atts:
                new_keys[k] = atts[akey]

    print("\nNew materials:")
    for material in new_materials:
        print(material)

    print("\nCandidates for additional material keys:")
    for k, v in new_keys.items():
        print("%s :: %s" % (k, v))