import pslink.quant as quant

quant.VolumeFormula.register(
    {
        "Peripheral Diameter": "d_outer",
        "Center Hole Diameter": "d_inner",
        "Cross-Sectional Height": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)
