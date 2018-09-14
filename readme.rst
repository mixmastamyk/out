
Out
===========

Simple, fun take on logging for non-huge projects. Gets "outta" the way.

(Why's are covered in the background_ section at the bottom.)

.. ~ TODO:
.. ~ HOWTO with Pygments
.. ~ pygments to 256 colors?
.. ~ document theme keyword plain, dict etc, uses std formatter
.. ~ console crashes on: p3 -m out.demos


Fun Features
--------------------------

First of all,
out is concise as hell,
basically a singleton logger ready on import.
In interactive mode:

.. code-block:: python

    >>> import out

    >>> out('And away we go…')  # configurable default level
    🅸 And away we go…

    >>> out.warn('Danger Will Robinson!')
    🆆 Danger Will Robinson!

(Imagine with nice ANSI colors. 😁)
Out has simple themes for message formats, styles, and icons.
Not to worry,
out is more conservative in production mode,
turned on automatically by redirecting ``stderr``::

    ⏵ python3 script.py |& cat
    2018-09-10 17:18:19.123 ✗ ERROR  Kerblooey!

Obvious defaults, and easy to configure!

.. code-block:: python

    >>> out.configure(
            level='note',           # or int
            default_level='info',   # out('…')
            datefmt='…',            # strftime
            msgfmt='…',             # see below
            stream=file,            # stderr
            theme=name|{},
            icons=name|{},          # see below
            style=name|{},          # about themes
            lexer='python3',        # highlight data
        )


.. note::

    This is a library to simplify logging for *applications.*

    Libraries should continue on as they always have:

    .. code-block:: python

        import logging

        log = logging.getLogger(__name__)
        # do not configure loggers, just use:
        log.debug('foo')


Colors, Unicode, Icons
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Colors are ready to go in interactive mode,
  and turn off automatically when output is redirected.

- Unicode symbols are used throughout as "icons" for increased readability and
  conciseness.

  They are/should be padded to two characters due to some glyphs being wide.
  Width can be looked up, e.g.::

    >>> unicodedata.east_asian_width('💀')
    'W'

- Syntax highlighting of data structures (oft parsed from JSON APIs) is
  available too, via Pygments.


Levels+
~~~~~~~~~~~~~~~~~~~~~~~~~~

While the
`standard levels <https://docs.python.org/3/library/logging.html#levels>`_
continue to exist
(``NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL``).
A few additions and slight modifications have been made.
These are commonly requested additions commonly poo-poo'd by core devs:

- ``TRACE``, for absurdly voluminous data, perhaps system calls or network
  traffic.

- ``NOTE``, for **positive** messages
  that should/must be shown by default---\
  unlike the standard warning,
  which could encourage the viewer to worry.  e.g.:

  | ``NOTE`` - Token is ABCXYZ, rather than…
  | ``WARNING`` - Token is ABCXYZ.

- ``EXCEPT``, to differentiate expected from unexpected errors.
  Think ``FileNotFound`` vs. ``Exception``.

- ``FATAL``, a renaming of ``CRITICAL``,
  since that name is long, pushes alignment,
  and does not capture message intent as well as fatal.
  Std-lib already allows this but still labels it critical on output.
  Out does not.



Log Template: msgfmt
~~~~~~~~~~~~~~~~~~~~~~~

By default out supports the ``{}`` formatting style,
as it is a bit easier to read.
Most fields are found in the Python
`logging docs. <https://docs.python.org/3/library/logging.html#logrecord-attributes>`_::

    {asctime}           Textual time when the LogRecord created.
    {msecs}             Millisecond portion of the creation time
    {filename}          Filename portion of pathname
    {funcName}          Function name
    {lineno)            Source line number where called.
    {levelno}           Numeric logging level for the message
    {levelname}         Text logging level for the message
    {pathname}          Full path of the source file called.
    {message}           The result of record.getMessage().
    {module}            Module (name portion of filename)
    {name}              Name of the logger (logging channel)

Use of
``out.format.ColorFormatter`` adds these additional fields::

    {on}{icon}{off}     Style and icon support.

For example:

.. code-block:: python

    out.configure(
        msgfmt='{on}{icon}{levelname:<7}{off} {message}'
    )


DateTime Format
++++++++++++++++++

These are configuable via
`strftime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>`_
syntax and the
``datefmt`` keyword to ``configure``.


Themes
~~~~~~~~~~~~~~~~~~

Themes are simply dictionaries with one entry per level:

.. code-block:: python

    >>> from out.themes import themes, icons, styles

    >>> icons['circled']  # Unicode
    {'TRACE': '🅣', 'DEBUG': '🅓', 'INFO': '🅘', 'WARNING': '🅦',
     'NOTE': '🅝', 'ERROR': '🅔', 'EXCEPT': '🅧', 'CRITICAL': '🅕',
     'FATAL': '🅕', 'NOTSET': '🅝'}

    >>> styles['blink']  # ANSI escapes
    {'TRACE': '\x1b[35m', 'DEBUG': '\x1b[34m', 'INFO': '\x1b[32m',
     'WARNING': '\x1b[93m', 'NOTE': '\x1b[96m', 'ERROR': '\x1b[31m',
     'EXCEPT': '\x1b[91m', 'CRITICAL': '\x1b[97m',
     'FATAL': '\x1b[97;5m', 'NOTSET': '\x1b[0m'}

The
`console <https://mixmastamyk.bitbucket.io/console/>`_
package is a good choice to generate ANSI styles:

.. code-block:: python

    from console import fg, bg, fx
    import out

    blue_note = dict(
        NOTE=str(fg.lightblue + fx.bold + fx.reverse),  # etc
    )
    out.configure(
        style=blue_note,
        msgfmt=bg.blue + '{asctime}' + fx.end + ' {message}',
    )
    out.note('John Coltrane')

A full theme is the whole kit together in a mapping—\
styles, icons, and templates:

.. code-block:: python

    >>> interactive = {
     'style': {},  # level:value mapping, see above
     'icons': {},  # level:value
     'fmt': '{asctime} {icon} {message}',  # message format
     'datefmt': '%H:%M:%S',  # date format,
    }

Using Themes
++++++++++++++

In the ``configure`` method of the out logger,
to use a theme from the themes module,
simply specify one by name:

.. code-block:: python

    >>> out.configure(
            theme='production',
        )

Or by setting a custom mapping:

.. code-block:: python

    >>> out.configure(
            theme=interactive,  # or, just icons:
            icons=dict(DEBUG='• ', INFO='✓ ', WARNING='⚠ ', ) # …
        )

A few themes are bundled:

Icons:
    ascii
    ascii_symbol
    circled
    circled_lower
    rounded
    symbol

Styles:
    norm
    bold
    blink (on fatal error)

Full themes:
    interactive
    production

    plain (Uses logging.Formatter for lower overhead.)


.. note::

    When there are conflicting arguments to the ``configure`` method,
    the last specified will win.
    This requires > Python 3.6, due to ordered keyword args.
    Below this version it is not recommended to do this since keyword order
    will be undefined and therefore the result.


Tips
---------

- By default the logger prints to ``stderr``.
  The reason being that when used in an interactive script normal application
  output may be easily segregated from log messages during redirection.

  Configurable via the ``stream`` keyword to ``.configure()``.

- Upgrading a long script from ``print()`` is easy::

    import out

    print = out.info  # or other level

- Perhaps some logging was already added, but you'd like to downsize.
  Add this to your main script::

    import out as logger


  A lot of code now doesn't need to change.

.. ~ - Want to keep your complex configuration but use the ``ColorFormatter`` class
  .. ~ and themes in your own project?

- The ``ColorFormatter`` class can be used in your own project:

  .. code-block:: python

    >>> from out.format import ColorFormatter

    >>> cf = ColorFormatter()
    >>> handler.setFormatter(cf)

- To print the logging configuration:

  .. code-block:: python

    >>> out.log_config()  # quotes to shut off highlighting:
    '''
    🅳  Logging config:
    🅳  / name: main, id: 139973461370360
    🅳    .level: trace (7)
    🅳    .default_level: info (20)
    🅳    + Handler: 0 <StreamHandler <stderr> (NOTSET)>
    🅳      + Formatter: <out.format.ColorFormatter object at 0x7f4e1c65efd0>
    🅳        .style: <logging.StrFormatStyle object at 0x7f4e1c65ef28>
    🅳        .datefmt: '%H:%M:%S'
    🅳        .msgfmt: '  {on}{icon}{off} {message}'
    '''

The logger in the main script file is named "main,"
also known as "root."


.. _background:

Background
--------------------------

If you're here it's very likely you already know that the Python standard
logging module is extremely flexible.
While awesome in theory,
it's unfortunately overkill for small to medium projects,
and these days many larger ones too.
Additionally,
its various Java-isms grate on the nerves,
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


Therefore,
for many (if not most) applications,
all the complexity and mumbo-jumbo in the logging package documentation about
multiple loggers with different levels, different handlers, formatters,
adapters, filters,
and complex configuration is flexibility at the *wrong level.*
In fairness,
this may not have always been the case,
and can still be helpful, perhaps on Windows.

Additionally, logging tools have also become standardized over time,
handling cross-language and cross-platform messages.
Imagine a pipeline where log events are routed and multiple tools can be
plugged in or out as needed—\
organization-wide rather than app-wide.

So, unless you have unique requirements,
there's no need to reimplement ``logrotate``, ``syslog``, ``systemd``, and
proprietary metrics tools in every programming language.
Just blast those logs to stdout/stderr and get logging *outta* the way!

Enter the ``out`` project.
It's ready to start logging from the get go.
It uses Python's standard logging infrastructure by default,
so is still quite flexible when need be.

Well, you've heard this before.
However, *out* tries a bit harder create a fun, easy-to-use interface,
as hopefully demonstrated above.

Name
~~~~~~~

Regarding the name,
well of course would have like to pick something along the lines of ``log`` but
all variations are long gone on PyPI.
``out()`` is a name I've often used over the years as a poor-man's logger—\
really a functional wrapper around ``print``,
until I could get around to adding proper logging.
Now we can continue the tradition.
The name is short, simple, and conceptually fits,
if a little bland.
