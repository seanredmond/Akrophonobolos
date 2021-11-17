from enum import IntFlag
from fractions import Fraction
import re

AMT = re.compile(r"\A((\d+)T ?)?((\d+)D ?)?((\d+(\.\d+)?)(O|B))?\Z", re.I)
GREEK_AMT = re.compile(
    r"\A[\u0394\u0397\u0399\u03a4\u03a7\U00010140-\U0001014E]+\Z")


class Fmt(IntFlag):
    GREEK = 16
    ENGLISH = 8
    ABBR = 4
    DECIMAL = 2
    FRACTION = 1


# Amounts are stored internally obols and can be fractional
# 1 talent = 36,000 obols
# 1 drachma = 6 obols

NUMERALS = {"\U0001014E": Fraction(180_000_000, 1),  # 𐅎 5000 TALENTS
            "\U0001014D":  Fraction(36_000_000, 1),  # 𐅍 1000 TALENTS
            "\U0001014C":  Fraction(18_000_000, 1),  # 𐅌 500 TALENTS
            "\U0001014B":   Fraction(3_600_000, 1),  # 𐅋 100 TALENTS
            "\U0001014A":   Fraction(1_800_000, 1),  # 𐅊 FIFTY TALENTS
            "\U00010149":     Fraction(360_000, 1),  # 𐅉 TEN TALENTS
            "\U00010148":     Fraction(180_000, 1),  # 𐅈 FIVE TALENTS
            "\U000003a4":      Fraction(36_000, 1),  # Τ TAU (1 talent)
            "\U00010146":      Fraction(30_000, 1),  # 𐅆 FIVE THOUSAND
            "\U000003a7":       Fraction(6_000, 1),  # Χ KHI (1000 drachmas)
            "\U00010145":       Fraction(3_000, 1),  # 𐅅 FIVE HUNDRED
            "\U00000397":         Fraction(600, 1),  # Η ETA (100 drachmas)
            "\U00010144":         Fraction(300, 1),  # 𐅄 FIFTY
            "\U00000394":          Fraction(60, 1),  # Δ DELTA (10 drachmas)
            "\U00010143":          Fraction(30, 1),  # 𐅃 FIVE
            "\U00010142":           Fraction(6, 1),  # 𐅂 ONE DRACHMA
            "\U00000399":           Fraction(1, 1),  # Ι IOTA (1 obol)
            "\U00010141":           Fraction(1, 2),  # 𐅁 ONE HALF
            "\U00010140":           Fraction(1, 4)   # 𐅀 ONE QUARTER
            }

FMT_TDO = (NUMERALS["Τ"], NUMERALS["𐅂"])

# # Not used:
# # 10147 𐅇 GREEK ACROPHONIC ATTIC FIFTY THOUSAND


class Khremata():
    def __init__(self, amt):
        self.qo = self._parse_amt(amt)

    def _parse_amt(self, amt):
        if isinstance(amt, Fraction):
            return amt
        
        if isinstance(amt, int):
            return amt * Fraction(4, 4)

        if isinstance(amt, float):
            return Fraction.from_float(amt) * Fraction(4, 4)
        

        if valid_greek_amount(amt):
            return parse_greek_amount(amt)

        if valid_amount_str(amt):
            return parse_amount(amt)

        raise Exception("UNHANDLED")


    def as_abbr(self, decimal=False):
        if decimal:
            return format_amount(self.qo, Fmt.ABBR | Fmt.DECIMAL)

        return format_amount(self.qo, Fmt.ABBR)

    
    def as_greek(self):
        return format_amount(self.qo.limit_denominator(4), Fmt.GREEK)


    def as_phrase(self, decimal=False):
        if decimal:
            return format_amount(self.qo, Fmt.ENGLISH | Fmt.DECIMAL)

        return format_amount(self.qo, Fmt.ENGLISH | Fmt.FRACTION)


    def __str__(self):
        return format_amount(self.qo, Fmt.ABBR | Fmt.FRACTION)


    def __repr__(self):
        return (f"{self.__class__.__name__} ("
                f"{self.__str__()} [= {float(self.qo)} obols])")


    def __int__(self):
        return int(self.qo.limit_denominator(1))


    def __float__(self):
        return float(self.qo)


    def __eq__(self, other):
        return self.qo == other
    

    def __ne__(self, other):
        return self.qo != other


    def __lt__(self, other):
        return self.qo < int(other)


    def ___le__(self, other):
        return self.qo <= int(other)


    def __gt__(self, other):
        return self.qo > int(other)


    def __ge__(self, other):
        return self.qo >= int(other)


    def __float__(self):
        return float(self.qo)


    def __add__(self, other):
        if isinstance(other, Khremata):
            return Khremata(self.qo + other.qo)

        return Khremata(float(self) + other)


    def __sub__(self, other):
        if isinstance(other, Khremata):
            return Khremata(self.qo - other.qo)

        return Khremata(float(self) - other)


    def __mul__(self, other):
        if isinstance(other, Khremata):
            return Khremata(self.qo * other.qo)

        return Khremata(self.qo * float(other))


    def __truediv__(self, other):
        # The units cancel out when an Akro id divided by an Akro, so
        # return a Fraction
        if isinstance(other, Khremata):
            return Khremata(self.qo / other.qo).qo

        # otherwise treat the divisor as a float and return an Akro
        return Khremata(self.qo / float(other))


    def __hash__(self):
        return hash(self.qo)


def _qo(*amt):
    """ Convert tuple amount to quarter obols. """
    return amt[0] * Fraction(36_000, 1) + amt[1] * Fraction(6, 1) + Fraction(amt[2])


def rec_reduce(amt, denominations):
    """Recursively reduce obols to t/d/o. """
    if denominations:
        return (amt // denominations[0],) + \
            rec_reduce(amt % denominations[0], denominations[1:])

    return (amt,)


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

    return _qo(talents, drachmas, obols)


def parse_greek_amount(amt):
    """ Parse Unicode Greek acrophonic numeral. """
    return sum([NUMERALS[c] for c in list(amt)])


def format_amount(amt, fmt_flags=Fmt.ABBR | Fmt.FRACTION):
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
    if not amt:
        return []

    num = [k for k, v in NUMERALS.items() if v <= amt][0]

    return [num] + _fmt_akrophonic(amt - NUMERALS[num])


def _fmt_fraction(amt):
    """ Format fractional obols as fractions. """
    if amt % 1 in (0.5, 0.25, 0.75):
        frac = {0.25: "¼", 0.5: "½", 0.75: "¾"}[amt % 1]
        whole = int(amt // 1) if amt // 1 else ""
        return f"{whole}{frac}"

    return int(amt)


def _fmt_decimal(amt):
    """ Format fractional obols as decimals. """
    if float(amt) % 1:
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
