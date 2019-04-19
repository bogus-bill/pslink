# pslink

pslink is an experimental project for the creation of product systems from
assembly part and component trees and the linking of the resulting processes
with LCI data from background databases like the
[LCA Commons](https://www.lcacommons.gov/). To achieve this, different
functions are implemented in `pslink` which are described in the following.


## Quantification
In order to combine the parts and components of the foreground system with
background data in a meaningful way, their dimensions and material composition
have to be quantified in some way. For standard parts and components there are
online databases, such as [PartTarget](http://www.parttarget.com), from which
such information can be retrieved. The corresponding masses can then be
estimated by the resulting volumes and material densities.

However, for different parts and components very different attributes that
describe their dimensions can occur. In order to solve this, volume formulas
can be dynamically registered in `pslink`, which determine the volume for a
given set of dimension attributes, e.g.:

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

For a set of properties of an assembly part (saved as key-value pairs), 
the function `volume_cm3(properties)` in the `pslink.quant` then searches
for a matching formula and calculates a volume. Length attributes, that `pslink`
understands, can be texts like `42.42 inches nominal` or even ranges like
`21.21 inches minimum and 42.42 inches maximum` (where the mean value is then
taken for calculating an estimated volume). With a set of corresponding
densities, the weights of the materials in an assembly part can be estimated.


## A semantic network of product relations

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
