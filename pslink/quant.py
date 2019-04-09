# estimating material quantities of a component from attribute-value pairs

import logging
import re


def length_cm(s: str) -> float:
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
        inches = match.group(1)
        try:
            return float(inches) * 2.54
        except:
            logging.error("failed to parse inches in: %s", s)
            return 0.0
    logging.error("no mathing pattern to extract length from: %s", s)
