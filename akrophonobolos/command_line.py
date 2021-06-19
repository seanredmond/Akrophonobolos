#!/usr/bin/env python3
import akrophonobolos as obol
import argparse
from enum import Enum, auto
from sys import exit

class UnexpectedEndOfEquation(Exception):
    pass

class INPUT_T(Enum):
    ACRO = auto()
    STR = auto()
    OP = auto()
    UNK = auto()


def detect_type(input):
    if any([i in obol.NUMERALS.keys() for i in input]):
        return INPUT_T.ACRO

    if input in ("+", "i"):
        return INPUT_T.OP

    return INPUT_T.UNK


def is_equation(input):
    return any([detect_type(i) == INPUT_T.OP for i in input])


def recurse_calc(eq):
    if len(eq) == 1:
        return parse_input_amount(eq[0])

        raise Exception("NON GREEK NOT UNHANDLED")

    if len(eq) > 1:
        if eq[1] == "+":
            return obol.reduce_amount(
                obol.add_amounts(parse_input_amount(eq[0]),
                                 recurse_calc(eq[2:])))
        raise Exception("SUBSTRACTION NOT HANDLED")

    raise UnexpectedEndofEquation()


def do_equation(input):
    result = recurse_calc(input)
    print(obol.format_amount(result))


def parse_input_amount(input):
    if detect_type(input) == INPUT_T.ACRO:
        return obol.reduce_amount(obol.parse_greek_amount(input))

    raise Exception("UNHANDLED")


def main():
    parser = argparse.ArgumentParser(
        description="Ancient Athenian acrophonic numeral converter"
        )
    parser.add_argument("input", nargs="+", type=str)
    args = parser.parse_args()

    if is_equation(args.input):
        do_equation(args.input)
        exit()

    for i in args.input:
        if detect_type(i) == INPUT_T.ACRO:
            p = obol.reduce_amount(obol.parse_greek_amount(i))
            print(f"{i} = {obol.format_amount(p)}")


if __name__ == "__main__":
    main()
