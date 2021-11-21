# Akrophonobolos

Python package for handling Ancient Athenian monetary values in
talents, drachmas and obols, including input and output in Greek
acrophonic numerals (such as 𐅎, 𐅍, 𐅌, 𐅋, 𐅊, etc.)

The denominations of Ancient Athenian money were the _tálanton_
(τάλαντον, or talent), the _drakhmḗ_ (δραχμή, or drachma), and the
_obolós_ (ὀβολός, or obol). Six _oboloí_ made a _drakhmḗ_, and 6,000
_drakhmaí_ a _tálanton_ (which was 57 lbs. of silver).

Large sums of money are found in forms like “1 _tálanton_ 813
_drakhmaí_ 1½ _oboloí_.” Math with these figures can be very annoying,
so Akrophonobolos simpfifies this.

## Installation

    pip install akrophonobolos
    
## Usage

Akrophonobolos provides a class, `Khremata` (χρήματα, "money") and
function for manipulating instances of this class.

### Initializing

An instance of `Khremata` can be initialized in several different ways:

With a string that gives amounts with the abbreviations `t`, `d`, and
`b` or `o`:

    >>> import akrophonobolos as obol
    >>> obol.Khremata("1t 813d 1.5b")
    Khremata (1t 813d 1½b [= 40879.5 obols])

You can use upper or lowercase letters, and spaces do not matter:

    >>> obol.Khremata("1T 813D 1.5B")
    Khremata (1t 813d 1½b [= 40879.5 obols])

    >>> obol.Khremata("1t813d1.5b")
    Khremata (1t 813d 1½b [= 40879.5 obols])
    
You can use `o` for obols, but since this is too similar to a zero,
`b` is better:

    >>> obol.Khremata("1t 813d 1.5o")
    Khremata (1t 813d 1½b [= 40879.5 obols])

    >>> obol.Khremata("1T 813D 1.5O")
    Khremata (1t 813d 1½b [= 40879.5 obols])
	
Internally, the `Khremata` class stores the value as a (possibly
fractional) number of _oboloí_, and this number can be used directly
to initialize an instance:

    >>> obol.Khremata(40879.5)
    Khremata (1t 813d 1½b [= 40879.5 obols])
	
Finally you can use a string of [Unicode Greek acrophonic
numerals](https://en.wikipedia.org/wiki/Ancient_Greek_Numbers_(Unicode_block)):

    >>> obol.Khremata("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    Khremata (1t 813d 1½b [= 40879.5 obols])
    
### Formatting

There are methods to format the value as an abbreviation, which is the
default string representation:

    >>> m = obol.Khremata("1t 813d 1.5b")
    >>> m.as_abbr()
    '1t 813d 1½b'
    >>> print(m)
    1t 813d 1½b
    
It can also be output as a phrase:

    >>> m.as_phrase()
    '1 talent, 813 drachmas, 1½ obols'
    
And as Greek numerals:

    >>> m.as_greek()
    'Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁'
    
### Math

You can do basic math with instances of `Khremata`

    >>> obol.Khremata("1t") + obol.Khremata("3000d")
    Khremata (1t 3000d [= 54000.0 obols])
    
    >>> obol.Khremata("1t") - obol.Khremata("3000d")
    Khremata (3000d [= 18000.0 obols])
    
    >>> obol.Khremata("1t") * 2
    Khremata (2t [= 72000.0 obols])
    
    >>> obol.Khremata("1t") / 2
    Khremata (3000d [= 18000.0 obols])

Comparisons:

    >>> obol.Khremata("1t") == obol.Khremata("1t")
    True
    
    >>> obol.Khremata("1t") > obol.Khremata("3000d")
    True
    
    >>> obol.Khremata("1t") < obol.Khremata("3000d")
    False
    
Most of these operators work both between two instance of `Khremata`
and between a `Khremata` and anything that can be converted into a
`Khremata`:

    >>> obol.Khremata("1t") + "3000d"
    Khremata (1t 3000d [= 54000.0 obols])
   
    >>> obol.Khremata("1t") - "ΧΧΧ"
    Khremata (3000d [= 18000.0 obols])
    
    >>> obol.Khremata("1t") == 36000
    True
    
    >>> 18000.0 < obol.Khremata("1t")
    True
    
You cannot multiply two instances of `Khremata` since "talents
squared" does not have any meaning (this raises an
`UndefinedMonetaryOperation` error). If you divide a `Khremata` by a
`Khremata` though the units cancel out and the operation returns a
unitless `Fraction`:

    >>> obol.Khremata("1500d") / obol.Khremata("1t")
    Fraction(1, 4)
    
### Fractions, part 1

Above, we said that the `Khremata` class stores the value internally
as a (possibly fractional) number of _oboloí_. The more correct way to
state that is that internally, the `Khremata` class stores the value,
in _oboloí_, as a Python
[Fraction](https://docs.python.org/3/library/fractions.html). You can
access this directly as the `b` property of the class. In many cases,
of course, this fraction is equivalent to a whole number (with a
denominator of 1):

    >>> m = obol.Khremata("100t")
    >>> m.b
    Fraction(3600000, 1)
    
But monetary sums could be recorded down to the quarter-obol:

    >>> m = obol.Khremata("1t 1d 1.25b")
    >>> m.b
    Fraction(144029, 4) 
    
which is the `Fraction` form of 36,007.25 _oboloí_. Storing the value
as a `Fraction` avoids some issues with floating point math and better
approximates how Ancient Greeks did math, since they did not use
decimal numbers.


### Loans and Interest

Figures in _tálanta_, _drakhmaí_, and _oboloí_ are found in many
ancient Athenian inscriptions, and the most interesting of these
involve loans, such as the so-called "Logistai Inscription" ([IG I³
369](https://epigraphy.packhum.org/text/381)) which records loans
from the money held in the Parthenon and temples of other gods to the
Athenian state. Loans were made at simple interest, most commonly at
the rate of 1 _drakhmḗ_ per 5 _tálanta_ per day.

Akrophonobolos provides functions for working with loans like this. To
start, you can calculate a more useful version of the rate. Given an
amount of principal, a number of days, and an amount of interest to be
returned, you get back the amount of simple interest to be added for
one day:

    >>> obol.interest_rate("5t", 1, "1d")
    Fraction(1, 30000)
    
That is, the interest is 1/30,000th of the principal per day.
    
For any loan, the amount of interest is simply the principal times the
rate times the term of the loan. If we borrowed 25 _tálanta_ for a
year at the common rate we would be expected to pay 1,825 _drakhmaí_ of
interest:

    >>> rate = obol.interest_rate("5t", 1, "1d")
    >>> obol.Khremata("25t") * rate * 365
    Khremata (1825d [= 10950.0 obols])
    
Of course Akrophonobolos has a function for this:

    >>> rate = obol.interest_rate("5t", 1, "1d")
    >>> obol.interest(obol.Khremata("25t"), 365, rate)
    Khremata (1825d [= 10950.0 obols])

1/30000th is the default rate, so you can leave it out if that's
the rate you're using:

    >>> obol.interest(obol.Khremata("25t"), 365)
    Khremata (1825d [= 10950.0 obols])
    
And instead of an instance of `Khremata` you can provide something that can be turned into a `Khremata`:

    >>> obol.interest("25t", 365)
    Khremata (1825d [= 10950.0 obols])
    
If you have the interest and the rate, you can use those to get the principal:

    >>> obol.principal("1825d", 365)
    Khremata (25t [= 900000.0 obols])
	
If you have the principal and the interest, you can get the loan
term, in days:

    >>> obol.loan_term("25t", "1825d")
    365
    
This last scenario is what we usually find in the inscriptions. For
instance, line 7 of the Logistai Inscription records one loan as

> 𐅊· τόκος τούτον ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ

or "50 _tálanta_. Interest on this 2 _tálanta_ 1,970 _drakhmaí_." We
can plug these values into `loan_term()` and see the the loan was for
1,397 days, just under 4 years:

    >>> obol.loan_term("𐅊", "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ")
    1397
    
### Fractions, part 2: Rounding

Line 88 of the Logistai Inscription records another loan as 3,418
_drakhmaí_ 1 _obolós_, with interest of 1 _drakhmḗ_ 5½ _oboloí_:

> ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι, τόκος τούτο 𐅂ΙΙΙΙΙ𐅁

This loan, it turns out, was for just 17 days.

    >>> obol.loan_term("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", "𐅂ΙΙΙΙΙ𐅁")
    17
    
Now, if we want to double-check this:

    >>> obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17)
    Khremata (1d 5¾b [= 11.75 obols])
    
We get an answer that is ¼ _obolós_ too high (11.75 instead of
11.5). We do not know how the ancient Greeks did this math, how they
rounded, or what kind of approximations they used. The smallest unit
they recorded was ¼ _obolós_, so in Akrohobolos the `interest()` and
`principal()` functions round up to this by default. You can get an
unrounded answer:

    >>> obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17, roundup=False)
    Khremata (1d 5b [= 11.621766666666666 obols])
    
We can see what the precise fraction is:
    
    >>> precise = obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17, roundup=False)
    >>> precise.b
    Fraction(1635618250918339, 140737488355328)
    
1,635,618,250,918,339/140,737,488,355,328ths is a quite a
fraction. Clearly the Greeks did some approximating. Maybe you can
play around with Akrophonobolos and figure out how they arrived at
11.5 obols for this amount.

`loan_term()` rounds to the nearest integer, but you can change this as well:

	>>> term = obol.loan_term("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", "𐅂ΙΙΙΙΙ𐅁", roundoff=False)
    >>> term
    Fraction(345000, 20509)
    >>> float(term)
    16.82188307572285
    
## Command Line Scripts

Akrophonobolos provides two command line scripts: `obol` for
converting and simple math, and `logistes` for working with loans and
interest

### `obol`

If you give `obol` one or more amounts in either akrophonic numerals
or abbreviated with "t", "d" and "b" (or "o"), it will show the
equivalent forms

    $ obol 𐅉𐅉𐅈 348d "1d 5.5b" 14T1800D4O
    𐅉𐅉𐅈 = 25 talents
    348d = ΗΗΗΔΔΔΔ𐅃𐅂𐅂𐅂
    1d 5.5b = 𐅂ΙΙΙΙΙ𐅁
    14T1800D4O = 𐅉ΤΤΤΤΧ𐅅ΗΗΗΙΙΙΙ
    
You can also give `obol` numbers to add and subtract

    $ obol 1t + 1000d
    ΤΧ = 1t 1000d
    $ obol 1t - 1000d
    𐅆 = 5000d

### `logistes`

`logistes` will calculate principal, interest or loan terms based on
its inputs (`-p` for principal, `-i-` for interest, '`-d` for days of
loan):

    $ logistes -p 50t -d 1397
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    $ logistes -p 50t -i ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    $ logistes -d 1397 -i ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    
By default the rate is the common one, 5 _tálanta_ yield 1 _drakhmḗ_
in one day. You can change this with `--int-p`, `--int-i`, and
`--int-d`. To calculate the above at _2 drakhmaí_ per day per 5
_tálanta_:

    $ logistes -p 50t -d 1397 --int-p 5t --int-i 2d --int-d 1
    𐅊 (50t) at 20 drachmas per day for 1397 days = ΤΤΤΤΧΧΧ𐅅ΗΗΗΗΔΔΔΔ (4t 3940d) interest

## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/seanredmond/akrophonobolos

