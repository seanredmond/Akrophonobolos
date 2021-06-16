import re

AMT = re.compile(r"((\d+)T)?((\d+)D)?((\d+(\.\d+)?)O)?")

NUMERALS = {"\U000003a4": (1,   0, 0.0),
            "\U00010145": (0, 500, 0.0),
            "\U00000397": (0, 100, 0.0),
            "\U00000394": (0,  10, 0.0),
            "\U00010142": (0,   1, 0.0),
            "\U00000399": (0,   0, 1.0),
            "\U00010141": (0,   0, 0.5)}


def add_amounts(*amts):
    """ Recursive memberwise addition of tuples. """
    if len(amts) == 0:
        return (0, 0, 0)

    return tuple([a + b for a, b in zip(amts[0], add_amounts(*amts[1:]))])


def reduce_amount(amt):
    return _reduce_drachmas((_reduce_obols(amt)))


def _reduce_drachmas(amt):
    return add_amounts((amt[0], 0, amt[2]),
                       (amt[1] // 6000, amt[1] % 6000, 0))


def _reduce_obols(amt):
    return add_amounts((amt[0], amt[1], 0),
                       (0, int(amt[2] // 6), amt[2] % 6))

    

def parse_amount(amt):
    """ Parse an Athenian currency string into a tuple. """

    amt_match = AMT.match(amt)
    talents = 0 if amt_match[2] is None else int(amt_match[2])
    drachmas = 0 if amt_match[4] is None else int(amt_match[4])
    obols = 0 if amt_match[6] is None else float(amt_match[6])

    return (talents, drachmas, obols)


def parse_greek_amount(amt):
    """ Parse Unicode Greek acrophonic numeral. """
    return add_amounts(*[NUMERALS[c] for c in list(amt)])
