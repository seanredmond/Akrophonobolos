import re

AMT = re.compile(r"((\d+)T)?((\d+)D)?((\d+(\.\d+)?)O)?")

NUMERALS = {"\U000003a4": (1,    0, 0.00), # Τ TAU (1 talent)
            "\U000003a7": (0, 1000, 0.00), # Χ KHI (1000 drachmas)
            "\U00000397": (0,  100, 0.00), # Η ETA (100 drachmas)
            "\U00000394": (0,   10, 0.00), # Δ DELTA (10 drachmas)
            "\U00000399": (0,    0, 1.00), # Ι IOTA (1 obol)
            "\U00010141": (0,    0, 0.50), # 𐅁 ONE HALF
            "\U00010140": (0,    0, 0.25), # 𐅀 ONE QUARTER
            "\U00010142": (0,    1, 0.00), # 𐅂 ONE DRACHMA
            "\U00010143": (0,    5, 0.00), # 𐅃 FIVE
            "\U00010144": (0,   50, 0.00), # 𐅄 FIFTY
            "\U00010145": (0,  500, 0.00), # 𐅅 FIVE HUNDRED
            "\U00010146": (0, 5000, 0.00), # 𐅆 FIVE THOUSAND
            "\U00010148": (5,    0, 0.00), # 𐅈 FIVE TALENTS
            "\U00010149": (10,   0, 0.00), # 𐅉 TEN TALENTS
            "\U0001014A": (50,   0, 0.00), # 𐅊 FIFTY TALENTS
            "\U0001014B": (100,  0, 0.00), # 𐅋 100 TALENTS
            "\U0001014C": (500,  0, 0.00), # 𐅌 500 TALENTS
            "\U0001014D": (1000, 0, 0.00), # 𐅍 1000 TALENTS
            "\U0001014E": (5000, 0, 0.00)  # 𐅎 5000 TALENTS
            }

    # Not used:
    # 10147 𐅇 GREEK ACROPHONIC ATTIC FIFTY THOUSAND

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
