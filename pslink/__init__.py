import pslink.linker
import pslink.quant as quant

# register volume formulas; formulas with more
# parameters should be registered first

quant.VolumeFormula.register(
    {
        "Grip Diameter": "gd",
        "Grip Length": "gl",
        "Nominal Thread Diameter": "td",
        "Thread Length": "tl",
    },
    "(pi / 4) * (gl * gd^2 + tl * td^2)"
)

quant.VolumeFormula.register(
    {
        "Overall Height": "h",
        "Bore Diameter": "d_inner",
        "End Diameter": "d_outer",
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)

quant.VolumeFormula.register(
    {
        "Width": "a",
        "Thickness": "b",
        "Length": "c"
    },
    "a * b * c"
)

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
        "Thread Length": "t_length",
        "Fastener Length": "f_length",
        "Nominal Thread Diameter": "t_diameter",
        "Hole Diameter": "hole_diameter",
        "Head Diameter": "head_d",
        "Head Height": "head_h"
    },
    "(pi / 4) * (head_h * head_d^2 + t_length * " +
    "t_diameter^2 + f_length * head_d^2)"
)

quant.VolumeFormula.register(
    {
        "Thread Length": "t_length",
        "Fastener Length": "f_length",
        "Head Height": "head_h",
        "Shoulder Diameter": "s_diameter",
        "Shoulder Length": "s_length",
        "Nominal Thread Diameter": "t_diameter",
    },
    "(pi / 4) * (head_h * s_diameter^2 + t_length * " +
    "t_diameter^2 + f_length * s_diameter^2)"
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
        "Outside Diameter": "d_outer",
        "Inside Diameter": "d_inner",
        "Material Thickness": "h"
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
        "Cross-Sectional Height": "h",
        "Peripheral Diameter": "d",
    },
    "(pi / 4) * h * d^2"
)

quant.VolumeFormula.register(
    {
        "Overall Height": "h",
        "Washer Outside Diameter": "d",
    },
    "(pi / 4) * h * d^2"
)

quant.VolumeFormula.register(
    {
        "Nut Height": "h",
        "Width Across Flats": "d",
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
        "Underloop Length": "h",
        "Diameter": "d",
    },
    "(pi / 4) * (2 * h) * d^2"
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

quant.VolumeFormula.register(
    {
        "Second End Outside Diameter Tube Accommodated": "d",
    },
    "(pi / 6) * d^3"
)


def link(data_dir: str, output="out.zip"):
    lin = pslink.linker.Linker(data_dir)
    lin.run(output)
