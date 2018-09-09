
Out
===========

*Out is a significantly simplified logger for Python3,
while a bit more powerful and fun in a few minor areas.*

Fun Features
--------------------------

Concise as hell::

    >>> import out

    >>> out('And away we go…')
    🅸 And away we go…

    >>> out.configure(foo='bar')


With nice colors.


Background
--------------------------

If you're here it's very likely you already know that the Python standard
logging module is extremely flexible.
While great in general,
unfortunately it's complete overkill for small to medium projects,
and these days many larger ones too.
Additionally,
its Java-isms grate on the nerves,
accentuating a big enterprisey design.

Meanwhile,
the rise of
`12 Factor App <https://12factor.net/logs>`_
patterns for daemons and services
means that simply logging to stdout/err is expected and desired
for portability:

    A twelve-factor app never concerns itself with routing or storage of its
    output stream. It should not attempt to write to or manage logfiles.
    Instead, each running process writes its event stream, unbuffered, to
    stdout. During local development, the developer will view this stream in
    the foreground of their terminal to observe the app’s behavior.


Imagine a pipeline where log events are routed and multiple tools can be
plugged in or out as needed.
Therefore,
for most(?) applications,
all the complexity and mumbo-jumbo in the logging package documentation about
multiple loggers with different levels, different handlers, formatters,
filters,
and complex configuration turned out to be flexibility at the wrong level.
In fairness,
this may not have always been the case,
and can still be helpful, perhaps on Windows.
Logging tools have also become more standardized over time.

So, unless you have unique requirements,
there's no need to reimplement ``logrotate``, ``syslog``, ``systemd``, and
proprietary metrics tools in every programming language.
Just blast those logs to stdout/stderr and get outta the way!
Enter *out*.

*Out* is ready to start logging on import.
It uses Python's standard infrastructure by default,
so is still quite configurable when neeeded.

Well, you've heard this before.
However, *out* tries a bit harder create an elegant interface.


.. note::

    This is a logging simplification library for *applications.*

    Libraries should continue as they always have::

        import logging

        log = logging.getLogger(__name__)

        # do not configure a logger, just use it:
        log.debug('foo')


Regarding the name,
wanted to pick something along the lines of ``log`` but all variations are
long gone on PyPI.
``out()`` is a name I've used over the years as a poor-man's logger,
really a functional wrapper around ``print``.
Short, simple, conceptually fits,
if a little bland.


Colors, Unicode, Icons
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Colors are ready to go in interactive mode,
  and turn off automatically as well.

- Syntax highlighting of data structures (say from JSON APIs) is available too,
  via Pygments.

- Unicode symbols for "icons" are used throughout for increased readability and
  conciseness.

  They are/should be padded to two characters due to some being wide.
  (Custom characters can be looked up with ``unicodedata.east_asian_width()``.)


.. ~ widths
.. ~ ++++++++

.. ~ ::

    .. ~ import unicodedata

    .. ~ >>> unicodedata.east_asian_width('a')
    .. ~ 'Na'

    .. ~ >>> unicodedata.east_asian_width('愛')
    .. ~ 'W'

    .. ~ >>> unicodedata.east_asian_width('💀')
    .. ~ 'W'

    .. ~ >>> unicodedata.east_asian_width('💣')
    .. ~ 'W'

    .. ~ >>> unicodedata.east_asian_width('Ⓓ')
    .. ~ 'A'



Levels
~~~~~~~~~~~~~~~~~~~~~~~~~~

While the
`standard levels <https://docs.python.org/3/library/logging.html#levels>`_
continue to exist,
a few additions and slight modifications have been made.
These are commonly requested additions commonly poo-poo'd by core devs:

- ``TRACE``, for absurdly voluminous data, perhaps network traffic.

- ``NOTE``, for **positive** messages
  that should/must be shown by default---\
  unlike the standard warning,
  which could encourage the viewer to worry.  e.g.:

  | ``WARNING`` - Token is ABCXYZ.
  | ``NOTE`` - Token is ABCXYZ.

- ``EXCEPT``, to differentiate the expected from unexpected errors.

- ``FATAL``, a renaming of ``CRITICAL``,
  since that name is long, awkward, and does not capture the intent well
  enough.
  Std-lib already allows this but labels it critical.



Tips
---------

- Upgrading from ``print``::

    import out

    print = out.info  # or other level

- Perhaps some logging was already added, but would like to simplify::

    import out as logger


  A lot of code now doesn't need to change.

- By default the logger prints to ``stderr``.
  The reason being that when used in an interactive script redirected output
  can be easily segregated from log messages.
  Configurable with the ``stream`` keyword.
