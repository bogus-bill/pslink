import pslink.quant as quant

# register volume formulas; formulas with more
# parameters should be registered first
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

quant.VolumeFormula.register(
    {
        "Overall Diameter": "d_outer",
        "Hole Diameter": "d_inner",
        "Thickness": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)

quant.VolumeFormula.register(
    {
        "Peripheral Diameter": "d_outer",
        "Center Hole Diameter": "d_inner",
        "Cross Section Outside Diameter": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)

quant.VolumeFormula.register(
    {
        "Length": "h",
        "Nominal Thread Size": "d",
    },
    "(pi / 4) * h * d^2"
)

quant.VolumeFormula.register(
    {
        "Length": "h",
        "Cross Section Outside Diameter": "d",
    },
    "(pi / 4) * h * d^2"
)

quant.VolumeFormula.register(
    {
        "Center Hole Diameter": "d_hole",
        "Cross-Sectional Height": "h",
    },
    "(pi / 4) * h * ((d_hole + h)^2 - d_hole^2)"
)

quant.VolumeFormula.register(
    {
        "Center Hole Diameter": "d_hole",
        "Cross-Sectional Height": "h",
    },
    "(pi / 4) * h * ((d_hole + h)^2 - d_hole^2)"
)

quant.VolumeFormula.register(
    {
        "Fastener Length": "h1",
        "Grip Length": "h2",
        "Shank Diameter": "d",
    },
    "(pi / 4) * (h1 + h2) * d^2"
)

quant.VolumeFormula.register(
    {
        "Rolling Element Diameter": "d",
    },
    "(pi / 6) * d^3"
)
