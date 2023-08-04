Class and Function Reference
============================

``Kremata`` Class
-----------------

This class represents a Greek monetary amount and provides for
formatting and mathematical operations.

.. autoclass:: akrophonobolos.Khremata
.. autofunction:: akrophonobolos.Khremata.__init__
.. autofunction:: akrophonobolos.Khremata.as_greek
.. autofunction:: akrophonobolos.Khremata.as_phrase
.. autofunction:: akrophonobolos.Khremata.as_abbr

Implemented special methods and operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: akrophonobolos.Khremata.__str__
.. autofunction:: akrophonobolos.Khremata.__repr__
.. autofunction:: akrophonobolos.Khremata.__int__
.. autofunction:: akrophonobolos.Khremata.__float__
.. autofunction:: akrophonobolos.Khremata.__eq__
.. autofunction:: akrophonobolos.Khremata.__ne__
.. autofunction:: akrophonobolos.Khremata.__lt__
.. autofunction:: akrophonobolos.Khremata.__le__
.. autofunction:: akrophonobolos.Khremata.__gt__
.. autofunction:: akrophonobolos.Khremata.__ge__
.. autofunction:: akrophonobolos.Khremata.__add__
.. autofunction:: akrophonobolos.Khremata.__sub__
.. autofunction:: akrophonobolos.Khremata.__mul__
.. autofunction:: akrophonobolos.Khremata.__truediv__
.. autofunction:: akrophonobolos.Khremata.__hash__


Functions
---------
.. autofunction:: akrophonobolos.valid_greek_amount
.. autofunction:: akrophonobolos.valid_amount_str
.. autofunction:: akrophonobolos.parse_amount
.. autofunction:: akrophonobolos.loan_term
.. autofunction:: akrophonobolos.interest
.. autofunction:: akrophonobolos.principal
		  


Exceptions
----------
.. autoexception:: akrophonobolos.UndefinedMonetaryOperation
.. autoexception:: akrophonobolos.UnparseableMonetaryString
