import akrophonobolos as obol

def test_parse_amt():
    assert obol.parse_amount("1T") == (1, 0, 0)
    assert obol.parse_amount("813D") == (0, 813, 0)
    assert obol.parse_amount("1.5O") == (0, 0, 1.5)
    assert obol.parse_amount("1T813D") == (1, 813, 0)
    assert obol.parse_amount("1T1.5O") == (1, 0, 1.5)
    assert obol.parse_amount("813D1.5O") == (0, 813, 1.5)
    assert obol.parse_amount("1T813D1.5O") == (1, 813, 1.5)
