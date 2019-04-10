# estimating material quantities of a component from attribute-value pairs

import logging
import re

import sympy


class VolumeFormula(object):

    _formulas = []

    def __init__(self, attributes: dict, function: str):
        self.attributes = {}
        for k, v in attributes.items():
            self.attributes[k.strip().lower()] = v.strip()
        self.function = function

    def matches(self, bindings: dict) -> bool:
        if not isinstance(bindings, dict):
            return False
        keys = set([k.strip().lower() for k in bindings.keys()])
        for k in self.attributes.keys():
            if k not in keys:
                return False
        return True

    def get_cm3(self, bindings: dict) -> float:
        expr = sympy.sympify(self.function)
        for k, v in bindings.items():
            k = k.strip().lower()
            if k not in self.attributes:
                continue
            length = length_cm(v)
            symbol = self.attributes[k]
            expr = expr.subs(symbol, length)
        return expr.evalf()

    @staticmethod
    def register(attributes: dict, function: str):
        VolumeFormula._formulas.append(VolumeFormula(attributes, function))


def volume_cm3(bindings: dict) -> float:
    for f in VolumeFormula._formulas:
        if f.matches(bindings):
            return f.get_cm3(bindings)
    logging.error("Could not find a volume formula for %s", bindings)
    return 0


def length_cm(s: str) -> float:
    """ Extracts the length from the given string and returns it in centimetres.
        Currently only texts in the form `<number> inches` are supported. """
    if not isinstance(s, str):
        return 0.0

    # a range
    regex = r"([^\s]*) inches minimum and ([^\s]*) inches maximum"
    match = re.search(regex, s)
    if match is not None:
        try:
            mini = float(match.group(1))
            maxi = float(match.group(2))
            return 2.54 * (mini + maxi) / 2
        except:
            logging.error("failed to parse inches in: %s", s)
            return 0.0

    # single value
    regex = r"([^\s]*) inches"
    match = re.search(regex, s)
    if match is not None:
        try:
            inches = match.group(1)
            return float(inches) * 2.54
        except:
            logging.error("failed to parse inches in: %s", s)
            return 0.0

    regex = r"([^\s]*) feet"
    match = re.search(regex, s)
    if match is not None:
        try:
            feet = match.group(1)
            return float(feet) * 30.48
        except:
            logging.error("failed to parse feet in: %s", s)
            return 0.0

    logging.error("no mathing pattern to extract length from: %s", s)
    return 0.0
