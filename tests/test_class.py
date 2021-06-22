import akrophonobolos as obol


def test_init():
    # Initialize with string
    money = obol.Akro("1t 813d 1.5b")
    assert money.qo == 163_518

    # Initialized with Greek
    money = obol.Akro("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    assert money.qo == 163_518

    # Initialized with number
    money = obol.Akro(163_518)
    assert money.qo == 163_518

    money = obol.Akro(163_518.1)
    assert money.qo == 163_518


def test_str():
    money = obol.Akro("1t 813d 1.5b")
    assert f"{money}" == "1t 813d 1½b"


def test_repr():
    money = obol.Akro("1t 813d 1.5b")
    assert money.__repr__() == "Akro (1t 813d 1½b [= 163518 ¼-obols])"


def test_as_abbr():
    money = obol.Akro("1t 813d 1.5b")
    assert money.as_abbr() == "1t 813d 1½b"
    assert money.as_abbr(decimal=True) == "1t 813d 1.5b"


def test_as_greek():
    money = obol.Akro("1t 813d 1.5b")
    assert money.as_greek() == "Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁"


def test_as_phrase():
    money = obol.Akro("1t 813d 1.5b")
    assert money.as_phrase() == "1 talent, 813 drachmas, 1½ obols"
    assert money.as_phrase(decimal=True) == "1 talent, 813 drachmas, 1.5 obols"


def test_int():
    money = obol.Akro("1t 813d 1.5b")
    assert int(money) == 163_518


def test_eq():
    money = obol.Akro("1t 813d 1.5b")
    assert money == 163_518
    assert money == money
    assert money == obol.Akro("1t 813d 1.5b")
    assert not money == 5


def test_ne():
    money = obol.Akro("1t 813d 1.5b")
    assert money != 163
    assert not money != money
    assert money != obol.Akro("1t")


def test_add():
    money = obol.Akro("5000d")
    the_sum = money + money
    assert isinstance(the_sum, obol.Akro)
    assert int(the_sum) == 240_000
    assert the_sum.as_abbr() == "1t 4000d"

    assert money + 1 == 120_001
    assert money + 1.5 == 120_002


def test_sub():
    money = obol.Akro("1t 4000d") - obol.Akro("5000d")
    assert isinstance(money, obol.Akro)
    assert int(money) == 120_000
    assert money.as_abbr() == "5000d"


def test_mul():
    money = obol.Akro("5000d") * 2
    assert isinstance(money, obol.Akro)
    assert int(money) == 240_000
    assert money.as_abbr() == "1t 4000d"


def test_div():
    money = obol.Akro("1t 4000d") / 2
    assert isinstance(money, obol.Akro)
    assert int(money) == 120_000
    assert money.as_abbr() == "5000d"

    # an Akro divided by an Akro should return a float
    assert money/money == 1
    assert isinstance(money/money, float)


def test_interest():
    # Interest amounts from the beginning of IG I³ 369. Simple
    # interest of 1.2 obols per talent per day, or 1/30000th per day

    # IG I³ 369 l. 5-6
    principal = obol.Akro("𐅉𐅉")
    days = 1424
    interest = (principal / 30000) * days
    assert interest.as_abbr() == "5696d"
    assert interest.as_greek() == "𐅆𐅅Η𐅄ΔΔΔΔ𐅃𐅂"

    # IG I³ 369 l. 7
    principal = obol.Akro("𐅊")
    days = 1397
    interest = (principal / 30000) * days
    assert interest.as_abbr() == "2t 1970d"
    assert interest.as_greek() == "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ"

    # IG I³ 369 l. 12
    principal = obol.Akro("𐅋")
    days = 1197
    interest = (principal / 30000) * days
    assert interest.as_abbr() == "3t 5940d"
    assert interest.as_greek() == "ΤΤΤ𐅆𐅅ΗΗΗΗΔΔΔΔ"
