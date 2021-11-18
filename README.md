# Akrophonobolos

Python package for handling Ancient Athenian monetary values in
talents, drachmas and obols, including input and output in Greek
acrophonic numerals (such as 𐅎, 𐅍, 𐅌, 𐅋, 𐅊, etc.)

The denominations of Ancient Athenian money were the _tálanton_
(τάλαντον, or talent), the _drakhmḗ_ (δραχμή, or drachma), and the
_obolós_ (ὀβολός, or obol). Six _oboloí_ made a _drakhmḗ_, and 6,000
_drakhmaí_ a _tálanton_ (which was 57 lbs. of silver).

Large sums of money are found in forms like “1 _tálanton_ 813
_drakhmaí_ 1½ _oboloí_.” Math with these figure can be very annoying,
so Akrophonobolos simpfifies this.

## Installation

    pip install akrophonobolos
    
## Usage

Akrophonobols provides a class, `Khremata` (χρήματα, "money") and function for manipulating these.

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
    
You can use `o` for obols, but since this is too similar to a zero, `b` is better:

    >>> obol.Khremata("1t 813d 1.5o")
    Khremata (1t 813d 1½b [= 40879.5 obols])

    >>> obol.Khremata("1T 813D 1.5O")
    Khremata (1t 813d 1½b [= 40879.5 obols])
	
Internally, the `Khremata` class stores the value as a (possibly
fractional) number of _oboloí_, and this number can be used directly
to initialize an instance:

    >>> obol.Khremata(40879.5)
    Khremata (1t 813d 1½b [= 40879.5 obols])
	
Finally you can use a string of [Unicode Greek acrophonic numerals](https://en.wikipedia.org/wiki/Ancient_Greek_Numbers_(Unicode_block)):

    >>> obol.Khremata("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    Khremata (1t 813d 1½b [= 40879.5 obols])
    
### Formatting

There are methods to format the value as an abbreviation, which is the default string representation:

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
        
## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/seanredmond/akrophonobolos

