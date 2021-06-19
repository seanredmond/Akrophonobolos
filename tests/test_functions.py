import akrophonobolos as obol

def test_parse_amt():
    assert obol.parse_amount("1T") == (1, 0, 0)
    assert obol.parse_amount("813D") == (0, 813, 0)
    assert obol.parse_amount("1.5O") == (0, 0, 1.5)
    assert obol.parse_amount("1T813D") == (1, 813, 0)
    assert obol.parse_amount("1T1.5O") == (1, 0, 1.5)
    assert obol.parse_amount("813D1.5O") == (0, 813, 1.5)
    assert obol.parse_amount("1T813D1.5O") == (1, 813, 1.5)


def test_parse_greek_amt():
    assert obol.parse_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁") == (1, 813, 1.5)
    assert obol.parse_greek_amount("ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ") == (2, 1970, 0)


def test_add_amounts():
    assert obol.add_amounts((1, 0, 0), (1, 0, 0)) == (2, 0, 0)
    assert obol.add_amounts((1, 0, 0), (0, 1, 0)) == (1, 1, 0)
    assert obol.add_amounts((1, 0, 0), (0, 0, 1)) == (1, 0, 1)
    assert obol.add_amounts((1, 1, 0), (1, 0, 0)) == (2, 1, 0)
    assert obol.add_amounts((1, 0, 0), (1, 1, 0)) == (2, 1, 0)
    assert obol.add_amounts((1, 1, 0), (1, 1, 0)) == (2, 2, 0)
    assert obol.add_amounts((1, 1, 1), (1, 1, 0)) == (2, 2, 1)
    assert obol.add_amounts((1, 1, 0), (1, 1, 1)) == (2, 2, 1)
    assert obol.add_amounts((1, 1, 1), (1, 1, 1)) == (2, 2, 2)
    
    assert obol.add_amounts(*(((1, 0, 0),) * 5)) == (5, 0, 0)
    assert obol.add_amounts(*(((1, 1, 1),) * 5)) == (5, 5, 5)

def test_reduce_amounts():
    assert obol.reduce_amount((0, 0, 7)) == (0, 1, 1)
    assert obol.reduce_amount((0, 6001, 0)) == (1, 1, 0)
    assert obol.reduce_amount((1, 0, 0)) == (1, 0, 0)

    assert obol.reduce_amount((0, 0, 6)) == (0, 1, 0)
    assert obol.reduce_amount((0, 0, 36000)) == (1, 0, 0)


def test_add_with_reducing():
    a = obol.parse_amount("20T")
    b = obol.parse_amount("50T")
    c = obol.parse_amount("28T5610D3.5O")
    d = obol.parse_amount("44T3000D")
    e = obol.parse_amount("100T")
    f = obol.parse_amount("18T3000D")

    assert obol.reduce_amount(
        obol.add_amounts(a, b, c, d, e, f)) == (261, 5610, 3.5)


    u = obol.parse_amount("5696D")
    v = obol.parse_amount("2T1970D")
    w = obol.parse_amount("1T1719D2O")
    x = obol.parse_amount("1T4700D1O")
    y = obol.parse_amount("3T5940D")
    z = obol.parse_amount("4173D4O")

    assert obol.reduce_amount(
        obol.add_amounts(u, v, w, x, y, z)) == (11, 199, 1.0)


def test_format_amount():
    assert obol.format_amount((1, 1, 1)) == "1 talent, 1 drachma, 1 obol"
    assert obol.format_amount((2, 2, 2)) == "2 talents, 2 drachmas, 2 obols"
    assert obol.format_amount((2, 0, 2)) == "2 talents, 2 obols"
    assert obol.format_amount((2, 2, 2.5)) == "2 talents, 2 drachmas, 2½ obols"
    assert obol.format_amount((2, 2, 1.25)) == "2 talents, 2 drachmas, 1¼ obols"
    assert obol.format_amount((2, 2, 0.25)) == "2 talents, 2 drachmas, ¼ obol"


def test_subtract_amounts():
    assert obol.subtract_amounts((5, 0, 0), (3, 0, 0)) == (2, 0, 0)
    assert obol.subtract_amounts((5, 0, 0), (0, 3000, 0)) == (4, 3000, 0)
    assert obol.subtract_amounts((5, 0, 0), (0, 0, 5)) == (4, 5999, 1)


def test_valid_amount_str():
    assert obol.valid_amount_str("1T")
    assert not obol.valid_amount_str("1Z")
    assert obol.valid_amount_str("261T5600D")
