import re

AMT = re.compile(r"((\d+)T)?((\d+)D)?((\d+(\.\d+)?)O)?")


def parse_amount(amt):
    """ Parse an Athenian currency string into a tuple. """

    amt_match = AMT.match(amt)
    talents = 0 if amt_match[2] is None else int(amt_match[2])
    drachmas = 0 if amt_match[4] is None else int(amt_match[4])
    obols = 0 if amt_match[6] is None else float(amt_match[6])

    return (talents, drachmas, obols)
