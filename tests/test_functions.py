import pytest
import akrophonobolos as obol

def test_parse_amt():
    assert obol.parse_amount("1T") == 144_000
    assert obol.parse_amount("813D") == 19_512_000
    assert obol.parse_amount("1.5O") == 6
    assert obol.parse_amount("1T813D") == 19_656_000
    assert obol.parse_amount("1T1.5O") == 144_006
    assert obol.parse_amount("813D1.5O") == 19_512_006
    assert obol.parse_amount("1T813D1.5O") == 19_656_006


def test_parse_amt_obol_rounding():
    assert obol.parse_amount("1O") == 4
    assert obol.parse_amount("0.9O") == 4

    assert obol.parse_amount("0.8O") == 3
    assert obol.parse_amount("0.75O") == 3
    assert obol.parse_amount("0.7O") == 3

    assert obol.parse_amount("0.6O") == 2
    assert obol.parse_amount("0.5O") == 2
    assert obol.parse_amount("0.4O") == 2

    assert obol.parse_amount("0.3O") == 1
    assert obol.parse_amount("0.25O") == 1
    assert obol.parse_amount("0.1O") == 0
    assert obol.parse_amount("0.3O") == 1


def test_parse_greek_amt():
    assert obol.parse_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁") == 163_518
    assert obol.parse_greek_amount("ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ") == 335_280


@pytest.mark.skip(reason="Not sure if this is needed")
def test_sum_amounts():
    assert obol.sum_amounts((1, 0, 0), (1, 0, 0)) == (2, 0, 0)
    assert obol.sum_amounts((1, 0, 0), (0, 1, 0)) == (1, 1, 0)
    assert obol.sum_amounts((1, 0, 0), (0, 0, 1)) == (1, 0, 1)
    assert obol.sum_amounts((1, 1, 0), (1, 0, 0)) == (2, 1, 0)
    assert obol.sum_amounts((1, 0, 0), (1, 1, 0)) == (2, 1, 0)
    assert obol.sum_amounts((1, 1, 0), (1, 1, 0)) == (2, 2, 0)
    assert obol.sum_amounts((1, 1, 1), (1, 1, 0)) == (2, 2, 1)
    assert obol.sum_amounts((1, 1, 0), (1, 1, 1)) == (2, 2, 1)
    assert obol.sum_amounts((1, 1, 1), (1, 1, 1)) == (2, 2, 2)
    
    assert obol.sum_amounts(*(((1, 0, 0),) * 5)) == (5, 0, 0)
    assert obol.sum_amounts(*(((1, 1, 1),) * 5)) == (5, 5, 5)


def test_reduce_amounts():
    assert obol.reduce_amount((0, 0, 7)) == (0, 1, 1)
    assert obol.reduce_amount((0, 6001, 0)) == (1, 1, 0)
    assert obol.reduce_amount((1, 0, 0)) == (1, 0, 0)

    assert obol.reduce_amount((0, 0, 6)) == (0, 1, 0)
    assert obol.reduce_amount((0, 0, 36000)) == (1, 0, 0)


@pytest.mark.skip(reason="Not sure if this is needed")
def test_add_with_reducing():
    a = obol.parse_amount("20T")
    b = obol.parse_amount("50T")
    c = obol.parse_amount("28T5610D3.5O")
    d = obol.parse_amount("44T3000D")
    e = obol.parse_amount("100T")
    f = obol.parse_amount("18T3000D")

    assert obol.reduce_amount(
        obol.sum_amounts(a, b, c, d, e, f)) == (261, 5610, 3.5)


    u = obol.parse_amount("5696D")
    v = obol.parse_amount("2T1970D")
    w = obol.parse_amount("1T1719D2O")
    x = obol.parse_amount("1T4700D1O")
    y = obol.parse_amount("3T5940D")
    z = obol.parse_amount("4173D4O")

    assert obol.reduce_amount(
        obol.sum_amounts(u, v, w, x, y, z)) == (11, 199, 1.0)


def test_format_amount_abbreviation():
    assert obol.format_amount(144_028) == "1t 1d 1b"
    assert obol.format_amount(288_056) == "2t 2d 2b"
    assert obol.format_amount(288_008) == "2t 2b"
    assert obol.format_amount(288_058) == "2t 2d 2½b"
    assert obol.format_amount(288_053) == "2t 2d 1¼b"
    assert obol.format_amount(288_049) == "2t 2d ¼b"

    # Abbreviation is the default
    assert obol.format_amount(144_028, obol.Fmt.ABBR) == \
        obol.format_amount(144_028)


def test_format_amount_abbreviation_decimal():
    assert obol.format_amount(144_028, obol.Fmt.DECIMAL) == "1t 1d 1b"
    assert obol.format_amount(288_056, obol.Fmt.DECIMAL) == "2t 2d 2b"
    assert obol.format_amount(288_008, obol.Fmt.DECIMAL) == "2t 2b"
    assert obol.format_amount(288_058, obol.Fmt.DECIMAL) == "2t 2d 2.5b"
    assert obol.format_amount(288_053, obol.Fmt.DECIMAL) == "2t 2d 1.25b"
    assert obol.format_amount(288_049, obol.Fmt.DECIMAL) == "2t 2d 0.25b"


def test_format_greek():
    assert obol.format_amount(163_518, obol.Fmt.GREEK) == "Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁"
    assert obol.format_amount(335_280, obol.Fmt.GREEK) == "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ"


def test_format_amount_english():
    assert obol.format_amount(144_028, obol.Fmt.ENGLISH) == \
        "1 talent, 1 drachma, 1 obol"
    assert obol.format_amount(288_056, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 2 obols"
    assert obol.format_amount(288_008, obol.Fmt.ENGLISH) == \
        "2 talents, 2 obols"
    assert obol.format_amount(288_058, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 2½ obols"
    assert obol.format_amount(288_053, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 1¼ obols"
    assert obol.format_amount(288_049, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, ¼ obol"


def test_format_amount_english_decimal():
    assert obol.format_amount(144_028, obol.Fmt.ENGLISH|obol.Fmt.DECIMAL) == \
        "1 talent, 1 drachma, 1 obol"
    assert obol.format_amount(288_056, obol.Fmt.ENGLISH|obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 2 obols"
    assert obol.format_amount(288_008, obol.Fmt.ENGLISH|obol.Fmt.DECIMAL) == \
        "2 talents, 2 obols"
    assert obol.format_amount(288_058, obol.Fmt.ENGLISH|obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 2.5 obols"
    assert obol.format_amount(288_053, obol.Fmt.ENGLISH|obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 1.25 obols"
    assert obol.format_amount(288_049, obol.Fmt.ENGLISH|obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 0.25 obol"
    

def test_subtract_amounts():
    assert obol.subtract_amounts((5, 0, 0), (3, 0, 0)) == (2, 0, 0)
    assert obol.subtract_amounts((5, 0, 0), (0, 3000, 0)) == (4, 3000, 0)
    assert obol.subtract_amounts((5, 0, 0), (0, 0, 5)) == (4, 5999, 1)


def test_valid_amount_str():
    assert obol.valid_amount_str("1T")
    assert not obol.valid_amount_str("1Z")
    assert obol.valid_amount_str("261T5600D")


def test_valid_amount_str():
    assert obol.valid_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    assert not obol.valid_greek_amount("1Z")
