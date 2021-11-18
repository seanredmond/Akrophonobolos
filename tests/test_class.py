import akrophonobolos as obol
from fractions import Fraction


def test_init():
    # Initialize with string

    money = obol.Khremata("1t")
    assert money.b == Fraction(36000, 1)

    money = obol.Khremata("1d")
    assert money.b == Fraction(6, 1)

    money = obol.Khremata("1b")
    assert money.b == Fraction(1, 1)

    money = obol.Khremata("1.5b")
    assert money.b == Fraction(3, 2)

    money = obol.Khremata("0.5b")
    assert money.b == Fraction(1, 2)

    money = obol.Khremata("0.25b")
    assert money.b == Fraction(1, 4)

    money = obol.Khremata("0.125b")
    assert money.b == Fraction(1, 8)
    
    money = obol.Khremata("1t 813d 1.5b")
    assert money.b == Fraction(81759, 2)

    # Initialized with Greek
    money = obol.Khremata("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    assert money.b == Fraction(81759, 2)

    # Initialized with number
    money = obol.Khremata(40879.5)
    assert money.b == Fraction(81759, 2)

    money = obol.Khremata(40880)
    assert money.b == 40880
    
    money = obol.Khremata(163518.1)
    assert money.b == Fraction(5618439134432461, 34359738368)


def test_str():
    money = obol.Khremata("1t 813d 1.5b")
    assert f"{money}" == "1t 813d 1½b"


def test_repr():
    money = obol.Khremata("1t 813d 1.5b")
    print(f"MONEY: {money.__repr__()}")
    assert money.__repr__() == "Khremata (1t 813d 1½b [= 40879.5 obols])"


def test_as_abbr():
    money = obol.Khremata("1t 813d 1.5b")
    assert money.as_abbr() == "1t 813d 1½b"
    assert money.as_abbr(decimal=True) == "1t 813d 1.5b"


def test_as_greek():
    money = obol.Khremata("1t 813d 1.5b")
    assert money.as_greek() == "Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁"


def test_as_phrase():
    money = obol.Khremata("1t 813d 1.5b")
    assert money.as_phrase() == "1 talent, 813 drachmas, 1½ obols"
    assert money.as_phrase(decimal=True) == "1 talent, 813 drachmas, 1.5 obols"


def test_int():
    money = obol.Khremata("1t 813d 1.5b")
    assert int(money) == 40879


def test_float():
    money = obol.Khremata("1t 813d 1.5b")
    assert float(money) == 40879.5


def test_eq():
    money = obol.Khremata("1t 813d 1.5b")
    assert money == 40879.5
    assert money == money
    assert money == obol.Khremata("1t 813d 1.5b")
    assert money == "1t 813d 1.5b"
    assert not money == 5
    assert not money == "5b"


def test_ne():
    money = obol.Khremata("1t 813d 1.5b")
    assert money != 163
    assert not money != money
    assert money != obol.Khremata("1t")


def test_add():
    money = obol.Khremata("5000d")
    the_sum = money + money
    assert isinstance(the_sum, obol.Khremata)
    assert int(the_sum) == 60_000
    assert the_sum.as_abbr() == "1t 4000d"

    assert money + 1 == 30_001
    assert money + 1.5 == 30_001.5
    assert money + 1.1 == 30_001.1


def test_sub():
    money = obol.Khremata("1t 4000d") - obol.Khremata("5000d")
    assert isinstance(money, obol.Khremata)
    assert int(money) == 30_000
    assert money.as_abbr() == "5000d"


def test_mul():
    money = obol.Khremata("5000d") * 2
    assert isinstance(money, obol.Khremata)
    assert int(money) == 60_000
    assert money.as_abbr() == "1t 4000d"


def test_div():
    money = obol.Khremata("1t 4000d") / 2
    assert isinstance(money, obol.Khremata)
    assert money == 30_000
    assert money.as_abbr() == "5000d"

    # an Akro divided by an Akro should return a Fraction
    assert money/money == 1
    assert isinstance(money/money, Fraction)

    assert obol.Khremata('2000d')/obol.Khremata('4000d') == Fraction(1, 2)
    


def test_interest():
    # Interest amounts from the beginning of IG I³ 369. Simple
    # interest of 1.2 obols per talent per day, or 1/30000th per day

    # IG I³ 369 l. 5-6
    principal = obol.Khremata("𐅉𐅉")
    days = 1424
    interest = (principal / 30000) * days
    assert interest.as_abbr() == "5696d"
    assert interest.as_greek() == "𐅆𐅅Η𐅄ΔΔΔΔ𐅃𐅂"

    # IG I³ 369 l. 7
    principal = obol.Khremata("𐅊")
    days = 1397
    interest = (principal / 30000) * days
    assert interest.as_abbr() == "2t 1970d"
    assert interest.as_greek() == "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ"

    # IG I³ 369 l. 12
    principal = obol.Khremata("𐅋")
    days = 1197
    interest = (principal / 30000) * days
    assert interest.as_abbr() == "3t 5940d"
    assert interest.as_greek() == "ΤΤΤ𐅆𐅅ΗΗΗΗΔΔΔΔ"
