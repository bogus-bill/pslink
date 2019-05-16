# check that we can identify the materials of the components in the data folder
# and that we have a density value for each material (we need this to calculate
# the component masses)

import glob

import pslink.partatts as partatts

if __name__ == "__main__":

    # the known materials are the keys in the density file
    known_materials = partatts.from_file("../data/densities.txt").keys()

    files = 0
    errors = 0
    warnings = 0
    for fpath in glob.glob("../data/components/*.txt"):
        files += 1
        comp_atts = partatts.from_file(fpath)
        comp_materials = partatts.materials(comp_atts)

        if len(comp_materials) == 0:
            errors += 1
            print("error: could not find materials in %s" % fpath)
            continue

        for mat in comp_materials:
            if mat not in known_materials:
                print("found new material %s in %s" % (mat, fpath))
                warnings += 1

    print("scanned materials in %i files: %i errors and %i warnings" %
          (files, errors, warnings))
