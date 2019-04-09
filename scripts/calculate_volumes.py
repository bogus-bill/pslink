import glob

import pslink.quant as quant

if __name__ == "__main__":
    for fpath in glob.glob("../data/components/*.txt"):
        with open(fpath, "r", encoding="utf-8") as f:
            bindings = {}
            for line in f.read().splitlines():
                parts = line.split(";")
                bindings[parts[0].strip()] = parts[1].strip()
            vol_cm3 = quant.volume_cm3(bindings)
            if vol_cm3 == 0:
                print("error: no volume for file", fpath)
            else:
                print("ok: vol_cm3=%f in %s" % (vol_cm3, fpath))
