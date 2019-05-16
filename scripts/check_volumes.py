# check the volume calculation for the component in the data folder

import glob

import pslink.partatts as partatts
import pslink.quant as quant

if __name__ == "__main__":
    for fpath in glob.glob("../data/components/*.txt"):
        atts = partatts.from_file(fpath)
        vol_cm3 = quant.volume_cm3(atts)
        if vol_cm3 == 0:
            print("error: no volume for file", fpath)
        else:
            print("ok: vol_cm3=%f in %s" % (vol_cm3, fpath))
