# Akrophonobolos

Python package for handling Ancient Athenian monetary values in
talents, drachmas and obols, including input and output in Greek
acrophonic numerals (such as 𐅎, 𐅍, 𐅌, 𐅋, 𐅊, etc.)


## Installation

    pip install akrophonobolos
    
## Usage

Read the full documentation on [Read the Docs](https://akrophonobolos.readthedocs.io/en/latest/)

Akrophonobolos provides functions for parsing, manipulating, and
formatting Greek acrophonic numerals. It also provides a class,
`Khremata` encapsulating these methods. Interally, the python
`fractions` library is used to minimize issues caused by floating
point arithmetic.

    >>> import akrophonobolos as obol
    >>> cash = obol.parse_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    >>> cash
    Fraction(81759, 2)
    >>> obol.format_amount(cash)
    '1t 813d 1½b'
    >>> obol.format_amount(cash, obol.Fmt.ENGLISH)
    '1 talent, 813 drachmas, 1½ obols'
    >>> obol.format_amount(cash, obol.Fmt.GREEK)
	'Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁'
	>>> obol.format_amount(cash * 2)
	'2t 1626d 3b'
	
Using the class:

    >>> cash1 = obol.Khremata('1t')
	>>> cash2 = obol.Khremata('300d 3b')
	>>> cash1 + cash2
	Khremata (1t 300d 3b [= 37803.0 obols])
	>>> cash1 - cash2
	Khremata (5699d 3b [= 34197.0 obols])
	>>> cash1/cash2
	Fraction(12000, 601)
	
There are functions for working with the sort of interest we see in
inscriptions such as [IG I³
369](https://epigraphy.packhum.org/text/381).

    >>> rate = obol.interest_rate("5t", 1, "1d")
    >>> rate
    Fraction(1, 30000)
	>>> obol.loan_term("𐅊", "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ", rate)
	1397

The first line calculates the rate required for 1 drachma interest on
1 talent in 1 day. The last applies it to the amounts found on line 7
of that inscription for the principal (𐅊, 50 talents) and interest
(ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ, 2 talents 1,970 drachmas) to determine that the loan
term was 1,397 days.

This package also provides two command lin scripts. `obol` performs conversion and simple math:

    $ obol 𐅉𐅉𐅈 348d "1d 5.5b" 14T1800D4O
    𐅉𐅉𐅈 = 25 talents
    348d = ΗΗΗΔΔΔΔ𐅃𐅂𐅂𐅂
    1d 5.5b = 𐅂ΙΙΙΙΙ𐅁
    14T1800D4O = 𐅉ΤΤΤΤΧ𐅅ΗΗΗΙΙΙΙ

    $ obol 1t + 1000d
    ΤΧ = 1t 1000d
    $ obol 1t - 1000d
    𐅆 = 5000d

`logistes` does loan calculations:

    $ logistes -p 50t -d 1397
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    $ logistes -p 50t -i ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    $ logistes -d 1397 -i ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest

## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/seanredmond/akrophonobolos

