#!/usr/bin/env python3
import akrophonobolos as obol
import argparse
from enum import Enum, auto

class INPUT_T(Enum):
    ACRO = auto()
    STR = auto()
    UNK = auto()


def detect_type(input):
    if any([i in obol.NUMERALS.keys() for i in input]):
        return INPUT_T.ACRO

    return INPUT_T.UNK


def main():
    parser = argparse.ArgumentParser(
        description="Ancient Athenian acrophonic numeral converter"
        )
    parser.add_argument("input", nargs="+", type=str)
    args = parser.parse_args()

    for i in args.input:
        if detect_type(i) == INPUT_T.ACRO:
            p = obol.reduce_amount(obol.parse_greek_amount(i))
            print(f"{i} = {p}")


if __name__ == "__main__":
    main()
