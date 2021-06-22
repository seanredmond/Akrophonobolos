from enum import Enum, IntEnum, IntFlag, auto
import re

AMT = re.compile(r"\A((\d+)T)?((\d+)D)?((\d+(\.\d+)?)O)?\Z", re.I)
GREEK_AMT = re.compile(
    r"\A[\u0394\u0397\u0399\u03a4\u03a7\U00010140-\U0001014E]+\Z")

class DENOMINATION(IntEnum):
    T = 0
    D = 1
    O = 2


class Fmt(IntFlag):
    GREEK = 16
    ENGLISH = 8
    ABBR = 4
    DECIMAL = 2
    FRACTION = 1


D_STR = {DENOMINATION.T: "talent",
         DENOMINATION.D: "drachma",
         DENOMINATION.O: "obol"}

# Amounts are stored internally in ¼-obols.
# 1 talent = 144,000 ¼-obols
# 1 drachma = 24 ¼-obols

NUMERALS = {"\U0001014E": 720_000_000, # 𐅎 5000 TALENTS
            "\U0001014D": 144_000_000, # 𐅍 1000 TALENTS
            "\U0001014C":  72_000_000, # 𐅌 500 TALENTS
            "\U0001014B":  14_400_000, # 𐅋 100 TALENTS
            "\U0001014A":   7_200_000, # 𐅊 FIFTY TALENTS
            "\U00010149":   1_440_000, # 𐅉 TEN TALENTS
            "\U00010148":     720_000, # 𐅈 FIVE TALENTS
            "\U000003a4":     144_000, # Τ TAU (1 talent)
            "\U00010146":     120_000, # 𐅆 FIVE THOUSAND
            "\U000003a7":      24_000, # Χ KHI (1000 drachmas)
            "\U00010145":      12_000, # 𐅅 FIVE HUNDRED
            "\U00000397":       2_400, # Η ETA (100 drachmas)
            "\U00010144":       1_200, # 𐅄 FIFTY
            "\U00000394":         240, # Δ DELTA (10 drachmas)
            "\U00010143":         120, # 𐅃 FIVE
            "\U00010142":          24, # 𐅂 ONE DRACHMA
            "\U00000399":           4, # Ι IOTA (1 obol)
            "\U00010141":           2, # 𐅁 ONE HALF
            "\U00010140":           1, # 𐅀 ONE QUARTER
            }

FMT_TDO = (NUMERALS["Τ"], NUMERALS["𐅂"])

# Not used:
# 10147 𐅇 GREEK ACROPHONIC ATTIC FIFTY THOUSAND


def sum_amounts(*amts):
    """ Recursive memberwise addition of tuples. """
    if len(amts) == 0:
        return (0, 0, 0)

    return tuple([a + b for a, b in zip(amts[0], sum_amounts(*amts[1:]))])

def _qo(amt):
    """ Convert tuple amount to quarter obols. """
    return amt[0] * 144_000 + amt[1] * 24_000 + round(amt[2] * 4)


def obolize(amt):
    """ Convert currency about to all obols """
    return (0, 0, (amt[0] * (6000 * 6)) + (amt[1] * 6) + amt[2])


def subtract_amounts(left, right):
    return reduce_amount((0, 0, obolize(left)[2] - obolize(right)[2]))


def reduce_amount(amt):
    return _reduce_drachmas((_reduce_obols(amt)))


def _reduce_drachmas(amt):
    return sum_amounts((amt[0], 0, amt[2]),
                       (amt[1] // 6000, amt[1] % 6000, 0))


def _reduce_obols(amt):
    return sum_amounts((amt[0], amt[1], 0),
                       (0, int(amt[2] // 6), amt[2] % 6))


def rec_reduce(amt, denominations):
    if denominations:
        return (amt // denominations[0],) + \
            rec_reduce(amt % denominations[0], denominations[1:])

    return (amt/4,)
                       
    
def valid_greek_amount(amt):
    return GREEK_AMT.search(amt) is not None


def valid_amount_str(amt):
    return AMT.search(amt) is not None


def parse_amount(amt):
    """ Parse an Athenian currency string into a tuple. """

    amt_match = AMT.match(amt)
    talents = 0 if amt_match[2] is None else int(amt_match[2])
    drachmas = 0 if amt_match[4] is None else int(amt_match[4])
    obols = 0 if amt_match[6] is None else float(amt_match[6])

    return _qo((talents, drachmas, obols))


def parse_greek_amount(amt):
    """ Parse Unicode Greek acrophonic numeral. """
    return sum([NUMERALS[c] for c in list(amt)])


def format_amount(amt, fmt_flags=Fmt.ABBR|Fmt.FRACTION):
    """ Format ¼-obols for readability """
    if fmt_flags & Fmt.GREEK:
        return "".join(_fmt_akrophonic(amt))
    

    if fmt_flags & Fmt.ENGLISH:
        return _fmt_tdo(rec_reduce(amt, FMT_TDO),
                        (("talent", "talents"), ("drachma", "drachmas"),
                         ("obol", "obols")),
                        _fmt_functions(fmt_flags),
                        " ", ", ")


    return _fmt_tdo(rec_reduce(amt, FMT_TDO),
                            (("t", "t"), ("d", "d"), ("b", "b")),
                            _fmt_functions(fmt_flags),
                            "", " ")


def _fmt_akrophonic(amt):
    if amt < 1:
        return []

    print(amt)

    num = [k for k, v in NUMERALS.items() if v <= amt][0]

    print(num)

    return [num] + _fmt_akrophonic(amt - NUMERALS[num])
    

def _fmt_fraction(amt):
    """ Format fractional obols as fractions. """
    if amt % 1 in (0.5, 0.25):
        frac = "½" if amt % 1 == 0.5 else "¼"
        whole = int(amt // 1) if amt // 1 else ""
        return f"{whole}{frac}"

    return int(amt)


def _fmt_decimal(amt):
    """ Format fractional obols as decimals. """
    if amt % 1:
        return float(amt)

    return int(amt)


def _fmt_functions(fmt_flags):
    """ Return a tuple of functions to be used to format TDO. """
    if fmt_flags & Fmt.DECIMAL:
        return (int, int, _fmt_decimal)
    return (int, int, _fmt_fraction)


def _fmt_plural(amt, denominations):
    if amt <= 1:
        return denominations[0]

    return denominations[1]

    
def _fmt_tdo(tdo, denominations, fmt_funcs, delim1, delim2):
    return delim2.join(
        [f"{func(amt)}{delim1}{_fmt_plural(amt, d)}"
         for amt, d, func in zip(tdo, denominations, fmt_funcs) if amt])


def _fmt_abbreviated(tdo, fmt_flags):
    return "".join(
        [f"{x[0]}{x[1]}" for x in zip(tdo, ("T", "D", "O")) if x[0]])


def _denomination_numerals(denomination):
    return [(k, v) for k, v in NUMERALS.items() if v[denomination] > 0]


def _format_greek_denomination(amt, denomination):
    return "".join(_recurse_denomination(
        amt, denomination, _denomination_numerals(denomination)))


def _recurse_denomination(amt, denomination, nums):
    if amt == 0:
        return ()

    d = [n for n in nums if n[1][denomination] <= amt][0]

    return (d[0],) + \
        _recurse_denomination(amt - d[1][denomination], denomination, nums)


def _format_denomination(amt, denomination):
    if amt == 0:
        return None

    if amt % 1 in (0.5, 0.25):
        frac = "½" if amt % 1 == 0.5 else "¼"
        whole = int(amt // 1) if amt // 1 else ""
        plural = "s" if amt > 1 else ""
        return f"{whole}{frac} {D_STR[denomination]}{plural}"

    return f"{int(amt)} {D_STR[denomination]}{'s' if amt != 1 else ''}"




    
