Usage
=====

Installation
------------

.. code-block:: console

   pip install akrophonobolos

Usage
-----

Greek currency amounts are recorded in *tálanta* ("talents"),
*drakhmaí* ("drachmas", 6000 to 1 *tálanta*), and *oboloí* ("obols", 6
to 1 *drakhmḗ*). These amounts are usually written in acrophonic
numerals such as 𐅋 (100 *tálanta*), 𐅄 (50 *drakhmaí*), or 𐅀 (¼
*obolós*). It is very cumbersome to try to do calculations with these
numbers. For example the number Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁 has to be worked out as 1
talent + 50 drachmas + (100 drachmas × 3) + 10 drachmas + (1 obols
× 3) + half an obol. Altogether, that's 1 talent, 813 drachmas, 1½
obols.

It's even more challenging to do math with these
numbers. :py:mod:`akrophonobolos` provides functions for parsing,
manipulating, and formatting these amounts.

After importing the package (suggest importing it as `obol`):

>>> import akrophonobolos as obol

You can parse a string of Unicode Greek acrophonic numerals:

>>> obol.parse_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
Fraction(81759, 2)

:py:mod:`akrophonobolos` also understands a format that uses "t" for
*tálanta*, "d" for *drakhmaí* and "o" or "b" *oboloí*. I recommend
using "b" since "o" looks to much like a "0":

>>> obol.parse_amount("1t 813d 1.5b")
Fraction(81759, 2)

This format is not case-sensitive and spaces don't matter

>>> obol.parse_amount("1T813D1.5B")
Fraction(81759, 2)

This format can also include Unicode vulgar fractions for ½ and ¼ *oboloí*:

>>> obol.parse_amount("1t 813d 1½b")
Fraction(81759, 2)

The amount is converted to a number of *oboloí* using the Python
`fractions <https://docs.python.org/3/library/fractions.html>`_
library. One *tálanta* is 36,000 *oboloí*, and 813 *drakhmaí* is
4,878, so our example amount is 36,000 + 4,878 + 1.5 = 40,879.5
*oboloí*. 81759/2 is the fractional way of saying 40879.5. Using
fractions avoids problems with floating point math and more closely
approximates the way these calculations would have been made in
ancient Greece.

This can be formatted:

>>> cash = obol.parse_amount("1t 813d 1½b")
>>> obol.format_amount(cash)
'1t 813d 1½b'

The default formatting is as an abbreviated phrase with fractions. You can output it as a decimal instead:

>>> obol.format_amount(cash, obol.Fmt.DECIMAL)
'1t 813d 1.5b'

As a full English phrase:

>>> obol.format_amount(cash, obol.Fmt.DECIMAL|obol.Fmt.ENGLISH)
'1 talent, 813 drachmas, 1.5 obols'

Or back to a Greek numeral:

>>> obol.format_amount(cash, obol.Fmt.GREEK)
'Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁'

These amounts can be used with any of the functions described below
but :py:mod:`akrophonobolos` also provides a class,
:py:class:`Khremata` (from χρήματα, "money") to make it easier to keep
track of and format the amounts.

:py:class:`Khremata` class
^^^^^^^^^^^^^^^^^^^^^^^^^^

An instance of :py:class:`Khremata` can be initialized with any of the string formats shown above:


>>> import akrophonobolos as obol
>>> obol.Khremata("1t 813d 1.5b")
Khremata (1t 813d 1½b [= 40879.5 obols])

>>> obol.Khremata("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
Khremata (1t 813d 1½b [= 40879.5 obols])

Or you can pass an :py:obj:`int`, :py:obj:`float`, or :py:obj:`Fraction`:

>>> obol.Khremata(40879.5)
Khremata (1t 813d 1½b [= 40879.5 obols])

    
Formatting
^^^^^^^^^^

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
    
Math
^^^^

You can do basic math with instances of :py:class:`Khremata`:

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
    
Most of these operators work both between two instance of :py:class:`Khremata`
and between a :py:class:`Khremata` and anything that can be converted into a
:py:class:`Khremata`:

>>> obol.Khremata("1t") + "3000d"
Khremata (1t 3000d [= 54000.0 obols])
   
>>> obol.Khremata("1t") - "ΧΧΧ"
Khremata (3000d [= 18000.0 obols])
    
>>> obol.Khremata("1t") == 36000
True
    
>>> 18000.0 < obol.Khremata("1t")
True
    
You cannot multiply two instances of :py:class:`Khremata` since "talents
squared" does not have any meaning (this raises an
`UndefinedMonetaryOperation` error). If you divide a `Khremata` by a
`Khremata`, though, the units cancel out and the operation returns a
unitless `Fraction`:

>>> obol.Khremata("1500d") / obol.Khremata("1t")
Fraction(1, 4)
    
Fractions, part 1
^^^^^^^^^^^^^^^^^

Above, we said that the :py:class:`Khremata` class stores the value internally
as a (possibly fractional) number of *oboloí*. The more correct way to
state that is that internally, the :py:class:`Khremata` class stores the value,
in *oboloí*, as a Python
`Fraction <https://docs.python.org/3/library/fractions.html>`_. You can
access this directly as the "b" property of the class. In many cases,
of course, this fraction is equivalent to a whole number (with a
denominator of 1):

>>> m = obol.Khremata("100t")
>>> m.b
Fraction(3600000, 1)
    
But monetary sums could be recorded down to the quarter-obol:

>>> m = obol.Khremata("1t 1d 1.25b")
>>> m.b
Fraction(144029, 4) 
    
which is the :py:class:`Fraction` form of 36,007.25 *oboloí*.


Loans and Interest
^^^^^^^^^^^^^^^^^^

Figures in *tálanta*, *drakhmaí*, and *oboloí* are found in many
ancient Athenian inscriptions, and the most interesting of these
involve loans, such as the so-called "Logistai Inscription" (`IG I³
369 <https://epigraphy.packhum.org/text/381>`_) which records loans
from the money held in the Parthenon and temples of other gods to the
Athenian state. Loans were made at simple interest, most commonly at
the rate of 1 *drakhmḗ* per 5 *tálanta* per day.

:py:mod:`akrophonobolos` provides functions for working with loans like this. To
start, you can calculate a more useful version of the rate. Given an
amount of principal, a number of days, and an amount of interest to be
returned, you get back the amount of simple interest to be added for
one day:

>>> obol.interest_rate("5t", 1, "1d")
Fraction(1, 30000)
    
That is, the interest is 1/30,000th of the principal per day.
    
For any loan, the amount of interest is simply the principal times the
rate times the term of the loan. If we borrowed 25 *tálanta* for a
year at the common rate we would be expected to pay 1,825 *drakhmaí* of
interest:

>>> rate = obol.interest_rate("5t", 1, "1d")
>>> obol.Khremata("25t") * rate * 365
Khremata (1825d [= 10950.0 obols])
    
Of course :py:mod:`Akrophonobolos` has a function for this:

>>> rate = obol.interest_rate("5t", 1, "1d")
>>> obol.interest(obol.Khremata("25t"), 365, rate)
Khremata (1825d [= 10950.0 obols])

1/30000th is the default rate, so you can leave it out if that's
the rate you're using:

>>> obol.interest(obol.Khremata("25t"), 365)
Khremata (1825d [= 10950.0 obols])
    
And instead of an instance of :py:class:`Khremata` you can provide
something that can be turned into a :py:class:`Khremata`:

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

    𐅊· τόκος τούτον ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ

or "50 *tálanta*. Interest on this 2 *tálanta* 1,970 *drakhmaí*." We
can plug these values into :py:func:`loan_term` and see the the loan
was for 1,397 days, just under 4 years:

>>> obol.loan_term("𐅊", "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ")
1397
    
Fractions, part 2: Rounding
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Line 88 of the Logistai Inscription records another loan as 3,418
*drakhmaí* 1 *obolós*, with interest of 1 *drakhmḗ* 5½ *oboloí*:

    ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι, τόκος τούτο 𐅂ΙΙΙΙΙ𐅁

This loan, it turns out, was for just 17 days.

>>> obol.loan_term("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", "𐅂ΙΙΙΙΙ𐅁")
17
    
Now, if we want to double-check this:

>>> obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17)
Khremata (1d 5¾b [= 11.75 obols])
    
We get an answer that is ¼-*obolós* too high (11.75 instead of
11.5). The :py:func:`interest` and :py:func:`principal` functions
round up to the nearest ¼-*obolós* by default. Sometimes this matches
the historical record sometimes is does not. You can get an unrounded
answer:

>>> obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17, roundup=False)
Khremata (1d 5b [= 11.621766666666666 obols])
    
Or we can see what the precise fraction is:
    
>>> precise = obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17, roundup=False)
>>> precise.b
Fraction(1635618250918339, 140737488355328)
    
1,635,618,250,918,339/140,737,488,355,328ths is a quite a
fraction. Clearly the Greeks did some approximating. Maybe you can
play around with :py:mod:`skrophonobolos` and figure out how they arrived at
11.5 obols for this amount.

:py:func:`loan_term()` rounds to the nearest integer, but you can
change this as well:

>>> term = obol.loan_term("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", "𐅂ΙΙΙΙΙ𐅁", roundoff=False)
>>> term
Fraction(345000, 20509)
>>> float(term)
16.82188307572285
    
Command Line Scripts
--------------------

Akrophonobolos provides two command line scripts: `obol` for
converting and simple math, and `logistes` for working with loans and
interest

obol
^^^^

If you give `obol` one or more amounts in either akrophonic numerals
or abbreviated with "t", "d" and "b" (or "o"), it will show the
equivalent forms

.. code-block:: console

    $ obol 𐅉𐅉𐅈 348d "1d 5.5b" 14T1800D4O
    𐅉𐅉𐅈 = 25 talents
    348d = ΗΗΗΔΔΔΔ𐅃𐅂𐅂𐅂
    1d 5.5b = 𐅂ΙΙΙΙΙ𐅁
    14T1800D4O = 𐅉ΤΤΤΤΧ𐅅ΗΗΗΙΙΙΙ
    
You can also give `obol` numbers to add and subtract

.. code-block:: console

    $ obol 1t + 1000d
    ΤΧ = 1t 1000d
    $ obol 1t - 1000d
    𐅆 = 5000d

logistes
^^^^^^^^

`logistes` will calculate principal, interest or loan terms based on
its inputs (`-p` for principal, `-i-` for interest, '`-d` for days of
loan):

.. code-block:: console

    $ logistes -p 50t -d 1397
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    $ logistes -p 50t -i ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    $ logistes -d 1397 -i ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    𐅊 (50t) at 10 drachmas per day for 1397 days = ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ (2t 1970d) interest
    
By default the rate is the common one, 5 *tálanta* yield 1 *drakhmḗ*
in one day. You can change this with `--int-p`, `--int-i`, and
`--int-d`. To calculate the above at 2 *drakhmaí* per day per 5
*tálanta*:

.. code-block:: console

    $ logistes -p 50t -d 1397 --int-p 5t --int-i 2d --int-d 1
    𐅊 (50t) at 20 drachmas per day for 1397 days = ΤΤΤΤΧΧΧ𐅅ΗΗΗΗΔΔΔΔ (4t 3940d) interest
