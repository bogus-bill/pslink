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


### A semantic network of product relations

The core component of `pslink` is a 
[semantic network](https://en.wikipedia.org/wiki/Semantic_network)
of products in which the following types of relations between these
products are stored:

* is exactly the same
* is more generic (is broader) 
* is more specific (is narrower)
* is derived from

In order to quickly create such a semantic product network, a simple,
text based, and from [WordNet](https://wordnet.princeton.edu/documentation/wninput5wn)
inspired data format with the following properties was developed:

* Each line contains the relationships of a product (the _subject_),
  which comes first, to one or several other products (the _objects_),
  which follow the subject in the same line.
* Product names are enclosed in quotation marks. The relationship
  of the subject to an object is indicated by a symbol at the end of
  the object's product name, where

  * `=` means `is same`
  * `^` means `is broader` (the inverse relation `is narrower` is
    automatically added)
  * `<` means `is derived from`

* Commas can be set as visual separators but are ignored like
  whitespaces. Lines that start with a `#` are ignored as
  comments.

The following example describes that "stainless steel" `is a`
"steel" and the `same as` "corrosion resistant steel", and
that a "steel product" `is a` "metal product" which is
`derived from` (made from) "steel".

```r
# a simple example
"stainless steel" ,  "corrosion resistant steel"=  ,  "steel"^
"steel product"   ,  "metal product"^              ,  "steel"<
```

The function `read_file` in the `semap` module parses such a
file and creates the corresponding graph data structure:


```python
import pslink.semap as semap

graph = semap.read_file("path/to/file.smapl")
```


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
