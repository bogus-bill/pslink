import glob

import pslink.partatts as partatts

if __name__ == "__main__":

    mat_atts = {"material", "iii material", "body material", "stem material",
                "seat material", "flow control device material",
                "spring material", "screw material"}

    new_keys = {}
    materials = set()
    for fpath in glob.glob("../data/components/*.txt"):
        atts = partatts.from_file(fpath)
        materials.update(partatts.materials(atts))
        for akey in atts.keys():
            k = akey.strip().lower()
            if "material" in k and k not in mat_atts:
                new_keys[k] = atts[akey]

    print("\nExtracted materials")
    for material in materials:
        print(material)

    print("\nCandidates for additional material keys:")
    for k, v in new_keys.items():
        print("%s :: %s" % (k, v))