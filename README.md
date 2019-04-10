# pslink

Given is a tree of (standard) components. Attributes, like dimensions and
used materials, of such components can be partly looked up via their part number
in online databases like [PartTarget](http://www.parttarget.com).


### Estimating the material composition of a component
The respective components can have very different attributes that describe
their dimensions. To estimate the volumes of such component, formulas for
different length attributes can be registered in the quantity module: 

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

For a set of key value pairs (`bindings`), that describe the attributes of a
component the function `quant.volume_cm3(bindings)` searches then for a
registered formula and calculates a volume. The length attributes
can be texts like `42.42 inches nominal` or even ranges like
`21.21 inches minimum and 42.42 inches maximum` (where the mean value is then
taken for calculating an estimated volume).

TODO:
* material density look up
* handle multi-material components
* generate material inputs in components


### Mapping of product and processes
The `symap` module contains a set of functions for mapping process and product
names based on string similarity measures which are specifically tuned to
work well with product and process names in LCI databases.

TODO:

* acyclic graph for storing and receiving semantic relations
* data format inspired by WordNet https://wordnet.princeton.edu/documentation/wninput5wn
  * `=` is same as
  * `^` is broader (we do not store narrower relations as they are just the inverse)


### Installation

```batch
rem get the project
cd <your project folder>
git clone https://github.com/msrocka/pslink.git
cd pslink

rem create a virtual environment and activate it
rem https://packaging.python.org/guides/installing-using-pip-and-virtualenv/
.\env\Scripts\activate
python -m virtualenv env
rem install the requirements
pip install -r requirements.txt
rem install the project
pip install -e .
```
