.. _thrift_binary_protocol:

Thrift Binary Protocol
======================

A description of Thrift's binary representation of all types and how these are
are send to a Thrift server.

This will mainly consist of code examples using Python's struct_ module.
``struct.pack`` is used to convert a Python value to binary data and vice versa
with ``struct.unpack``. All format characters need to be prefixed with an ``!``
(exclamation mark) (network/big-endian).

This document is based on Thrift 0.8.0.

.. _struct: http://docs.python.org/library/struct.html


Base Types
----------

Some basic types that are converted to their Python counterparts.

+-------------------------+------------------------+----------------------------+--------------------------+
| Thrift Type             | Python type            | Size in bytes              | Struct Format Characters |
+=========================+========================+============================+==========================+
| ``bool``                | ``bool``               | 1                          | ``b``                    |
+-------------------------+------------------------+----------------------------+--------------------------+
| ``byte``                | ``integer``            | 1                          | ``b``                    |
+-------------------------+------------------------+----------------------------+--------------------------+
| ``i16``                 | ``integer``            | 2                          | ``h``                    |
+-------------------------+------------------------+----------------------------+--------------------------+
| ``i32``                 | ``integer``            | 4                          | ``i``                    |
+-------------------------+------------------------+----------------------------+--------------------------+
| ``i64``                 | ``integer``            | 8                          | ``q``                    |
+-------------------------+------------------------+----------------------------+--------------------------+
| ``double``              | ``float``              | 8                          | ``d``                    |
+-------------------------+------------------------+----------------------------+--------------------------+
| ``string``              | ``string`` [1]_        | 8 + string length in bytes | ``i`` (only for length)  |
+-------------------------+------------------------+----------------------------+--------------------------+

.. [1] Only the length of the string is converted using ``struct.pack``. The
       string itself can just be appended to the (converted) length.


Structs
-------

TODO


Containers
----------

TODO


Exceptions
----------

TODO


Services
--------

TODO
