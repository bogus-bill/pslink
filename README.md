# pslink

Given is a tree of (standard) components. Attributes, like dimensions and
used materials, of such components can be partly looked up via their part number
in online databases like [PartTarget](http://www.parttarget.com).


### Estimating the material composition of a component
The respective components can have very different attributes that describe
their dimensions. To estimate the volume of a component, the quantity module
allows to flexibly register a formula for a set of length attributes that
calculates a volume in `cm3`: 

```python
import pslink.quant as quant

quant.VolumeFormula.register(
    {
        "Outside Diameter": "d_outer",
        "Center Hole Diameter": "d_inner",
        "Cross-Sectional Height": "h"
    },
    "(pi / 4) * h * (d_outer^2 - d_inner^2)"
)
```

For a set of key value pairs `bindings`, that describe the attributes of a
component the `quant.volume_cm3(bindings)` functions searches then for a
registered formula and calculates and calculates a volume. The length attributes
can be texts like `42.42 inches nominal` or even ranges like
`21.21 inches minimum and 42.42 inches maximum` where the mean value is then
taken for calculating an estimated volume.

TODO:

* material density look up
* multi-material components


### Syntactic mapping
The `symap` module contains a set of functions ...

* 

### Semantic mapping

The `semap` module ...

https://wordnet.princeton.edu/documentation/wninput5wn

* `=` is same as
* `^` is broader (we do not store narrower relations as they are just the inverse)
* (`<` is precursor)

### Installation

```
pip install -e .
```

Dependencies:

* https://www.sympy.org | https://pypi.org/project/sympy/
* https://github.com/jamesturk/jellyfish | https://pypi.org/project/jellyfish/
* olca-ipc


## Sources

* http://www.cs.utexas.edu/~ml/papers/marlin-kdd-03.pdf
* http://www.semantic-web-journal.net/system/files/swj1470.pdf
* https://www.kushaldave.com/p451-dave.pdf