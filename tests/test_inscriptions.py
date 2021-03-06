import akrophonobolos as obol
from fractions import Fraction
import pytest


def test_ig_I_3_369_7():
    # πΒ· ΟΟΞΊΞΏΟ ΟΞΏΟΟΞΏΞ½ Ξ€Ξ€Ξ§πΞΞΞΞπΞΞ
    assert obol.loan_term("π", "Ξ€Ξ€Ξ§πΞΞΞΞπΞΞ") == 1397
    assert obol.interest("π", 1397) == obol.Khremata("Ξ€Ξ€Ξ§πΞΞΞΞπΞΞ")
    assert obol.principal("Ξ€Ξ€Ξ§πΞΞΞΞπΞΞ", 1397) == obol.Khremata("π")


@pytest.mark.xfail(reason="Different from restorated text")
def test_ig_I_3_369_7_8():
    # π[ππΞ€Ξ€Ξ€ππΞΞΞΞΞπ]Β· ΟΟΞΊΞΏΟ ΟΞΏΟΟΞΏΞ½ Ξ€Ξ§πΞΞΞπππππΞΞ
    assert obol.principal("Ξ€Ξ§πΞΞΞπππππΞΞ", 1349) == "πππΞ€Ξ€Ξ€ππΞΞΞΞΞπ"


def test_ig_I_3_369_12():
    # πΒ· ΟΟΞΊΞΏΟ ΟΞΏΟΟΞΏΞ½ Ξ€Ξ€Ξ€ππΞΞΞΞΞΞΞΞ
    assert obol.loan_term("π", "Ξ€Ξ€Ξ€ππΞΞΞΞΞΞΞΞ") == 1197
    assert obol.interest("π", 1197) == obol.Khremata("Ξ€Ξ€Ξ€ππΞΞΞΞΞΞΞΞ")
    assert obol.principal("Ξ€Ξ€Ξ€ππΞΞΞΞΞΞΞΞ", 1197) == obol.Khremata("π")


def test_id_I_3_369_88():
    # Ξ§Ξ§Ξ§ΞΞΞΞΞππππΞ, ΟΟΞΊΞΏΟ ΟΞΏΟΟΞΏ πΞΞΞΞΞπ
    assert obol.loan_term("Ξ§Ξ§Ξ§ΞΞΞΞΞππππΞ", "πΞΞΞΞΞπ") == 17

    assert float(obol.loan_term("Ξ§Ξ§Ξ§ΞΞΞΞΞππππΞ", "πΞΞΞΞΞπ",
                                roundoff=False)) == 16.82188307572285

    assert obol.interest("Ξ§Ξ§Ξ§ΞΞΞΞΞππππΞ", 17, roundup=False) == \
        11.621766666666666

    assert obol.principal("πΞΞΞΞΞπ", 17, roundup=False) == 20294.11764705882


@pytest.mark.xfail(reason="Different rounding")
def test_id_I_3_369_88_rounded_interest():
    # 1d 5ΒΎb vs. 1d 5Β½b
    assert obol.interest("Ξ§Ξ§Ξ§ΞΞΞΞΞππππΞ", 17) == obol.Khremata("πΞΞΞΞΞπ")


@pytest.mark.xfail(reason="Different rounding")
def test_id_I_3_369_88_rounded_principal():
    # 3382d 2ΒΌb vs 3418d 1b
    assert obol.principal("πΞΞΞΞΞπ", 17) == obol.Khremata("Ξ§Ξ§Ξ§ΞΞΞΞΞππππΞ")
