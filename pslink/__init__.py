import pslink.quant as quant

quant.VolumeFormula.register(
    {
        "Outside Diameter": "d_outer",
        "Center Hole Diameter": "d_inner",
        "Cross-Sectional Height": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)

quant.VolumeFormula.register(
    {
        "Peripheral Diameter": "d_outer",
        "Center Hole Diameter": "d_inner",
        "Cross-Sectional Height": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)

quant.VolumeFormula.register(
    {
        "Body Outside Diameter": "d_outer",
        "Body Inside Diameter": "d_inner",
        "Overall Length": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)

quant.VolumeFormula.register(
    {
        "Outer Member Outside Diameter": "d_outer",
        "Bore Diameter": "d_inner",
        "Outer Member Width": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)
