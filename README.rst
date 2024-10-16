
Out
===========

Fun take on logging for non-huge projects—out gets "outta" the way!

Background
--------------------------

If you're here it's very likely you already know that the Python standard
logging module is extremely flexible,
and that's great.
Unfortunately, it is overkill for small to medium projects,
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

    *A twelve-factor app never concerns itself with routing or storage of its
    output stream. It should not attempt to write to or manage logfiles.
    Instead, each running process writes its event stream, unbuffered, to
    stdout. During local development, the developer will view this stream in
    the foreground of their terminal to observe the app’s behavior.*


Therefore,
for many (if not most) applications,
all the complexity and mumbo-jumbo in the logging package documentation about
multiple loggers with different levels, different handlers, formatters,
adapters, filters, rotation,
and complex configuration is flexibility at the *wrong level!*
 In fairness,
this may not have always been the case,
and can still be helpful, perhaps on Windows.

Additionally, logging tools have also become standardized over time,
handling cross-language and cross-platform messages.
Imagine a pipeline where log events are routed and multiple tools can be
plugged in or out as needed—\
organization-wide rather than app- or language-wide.

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
as discussed above.

**Naming**

Regarding the name,
well of course would have liked something along the lines of ``log`` but all
variations of that are *long gone* on PyPI.
``out()`` is a name I've often used over the years as a poor-man's logger—\
really a functional wrapper around ``print``,
until I could get around to adding proper logging.
Now, the tradition continues.
The name is short, simple, and conceptually fits,
if a little bland.

Features
------------

First of all,
out is concise as hell,
basically a singleton logger configuration ready on import.
In interactive mode:

.. code-block:: python-console

    >>> import out

    >>> out('And away we go…')  # configurable default level
    🅸 main/func:1 And away we go…

    >>> out.warn('Danger Will Robinson!')
    🆆 main/func:1 Danger Will Robinson!

(Imagine with nice ANSI colors. 😁)
Out has simple themes for message formats, styles, and icons.
Not to worry,
out is more conservative in "production mode,"
which may be turned on automatically by redirecting ``stderr``:

.. code-block:: shell

    ⏵ python3 script.py |& cat  # bash, for fish use: &|
    2018-09-10 17:18:19.123 ✗ ERROR main/func:1 Kerblooey!


.. note::

    This is a library to simplify logging configuration for *applications.*

    Libraries and independent modules should continue on logging *messages* as
    they always have:

    .. code-block:: python

        import logging

        log = logging.getLogger(__name__)

        # do not configure loggers, just use:
        log.debug('foo')


Colors, Highlighting, Unicode Icons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Colors are ready to go in interactive mode,
  and turn off automatically when output is redirected.

- Unicode symbols are used throughout as "icons" for increased readability and
  conciseness.

- Syntax highlighting of data structures (oft parsed from remote APIs) is
  available too, via Pygments.


Useful defaults, and easy to configure!

.. code-block:: python-console

    >>> out.configure(
            level='note',           # level messages passed: str/int
            default_level='info',   # when called w/o a method: out('…')
            datefmt='…',            # see strftime
            msgfmt='…',             # see logging and below
            stream=file,            # stderr is default

            theme=name|dict,        # see below
            icons=name|dict,        #   about themes
            style=name|dict,
            highlight=False,        # disable highlighting
            lexer='python3',        # choose lexer
        )

We'll go into more detail below.


Log Message Format
~~~~~~~~~~~~~~~~~~~

By default out supports the curly-brace ``{}`` formatting style for both the
log message format and message template,
as it is a bit easier to read than printf-style.
Field definitions are found in the Python
`logging docs <https://docs.python.org/3/library/logging.html#logrecord-attributes>`_::

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

Use of the
``out.format.ColorFormatter`` class adds these additional fields::

    {on}{icon}{off}     Per-level style and icon support.

For example:

.. code-block:: python

    out.configure(
        msgfmt='{on}{icon}{levelname:<7}{off} {message}',
    )


DateTime Format
++++++++++++++++++

These are configuable via the standard
`strftime <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>`_
syntax and the
``datefmt`` keyword to ``configure``.

.. code-block:: python

    out.configure(
        datefmt='%y-%m-%d %H:%M:%S',
    )


Message:
++++++++++++++++++

When writing messages, printf ``%`` formatting style is supported as well
due to compatibility requirements with a majority of libraries:

.. code-block:: python

    out.warn('foo: %s', bar)
    out.warn('foo: {}', bar)

The second form may be used also,
though it will be a tiny bit slower,
since the printf-style must be tried first.

You'll want to use one of these forms,
as (in logging) they skip formatting of the string when the message isn't
sent.


Levels++
~~~~~~~~~~~~~~~~~~~~~~~~~~

While the
`standard levels <https://docs.python.org/3/library/logging.html#levels>`_
continue to exist
(``NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL``).
A few additions and slight modifications have been made.
Commonly requested:

- ``TRACE``, for absurdly voluminous data, perhaps system calls or network
  traffic.

- ``NOTE``, for **positive** messages
  that should/must be shown by default---\
  unlike the standard warning,
  which could encourage the viewer to worry.  e.g.:

      | ``NOTE`` - Token is ABCXYZ, rather than…
      | ``WARNING`` - Token is ABCXYZ.

- ``EXCEPT``, to differentiate common from unexpected errors.
  Think ``FileNotFound`` vs. ``Exception``.

- ``FATAL``, an alias of ``CRITICAL``,
  since that name is long, pushes alignment,
  and does not capture intent as well as fatal.
  Std-lib already allows this but still labels it critical on output.
  Out does not.


Themes
~~~~~~~~~~~~~~~~~~


Icons and Styles
+++++++++++++++++

``out`` can be themed with icon sets and/or styles and are simply dictionaries
with one entry per level.


.. code-block:: python-console

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
package is a good choice to generate ANSI styles for the levels,
as well as styling other fields:

.. code-block:: python

    from console import fg, bg, fx
    import out

    blue_note = dict(
        NOTE=str(fg.lightblue + fx.bold + fx.reverse),
        # other levels…
    )
    out.configure(
        style=blue_note,  # ← level styles, ↓ field styles
        msgfmt=bg.blue('{asctime}') + ' {message}',
    )
    out.note('John Coltrane')


Creating and Using Themes
++++++++++++++++++++++++++

A full theme is the whole kit together in a mapping—\
styles, icons, ``message`` and/or ``datefmt`` templates:

.. code-block:: python-console

    >>> interactive_theme = {
     'style': {},  # level:value mapping, see above
     'icons': {},  # level:value
     'fmt': '{asctime} {icon} {message}',  # message format
     'datefmt': '%H:%M:%S',  # date/time format,
    }


In the ``configure`` method of the out logger,
to use a theme from the themes module,
simply specify an existing one by name:

.. code-block:: python-console

    >>> out.configure(
            theme='production',
        )

Or by setting a custom mapping, as created above:

.. code-block:: python-console

    >>> out.configure(
            theme=interactive_theme,  # or perhaps just icons:
            icons=dict(DEBUG='• ', INFO='✓ ', WARNING='⚠ ', ) # …
        )

A few themes are bundled:

Icons:
    ascii,
    ascii_symbol,
    circled,
    circled_lower,
    rounded,
    symbol

Styles:
    - norm
    - bold
    - mono (monochrome)
    - blink (fatal error only)

Full themes:
    - interactive
    - production
    - plain (Uses logging.Formatter for lower overhead.)
    - json (Uses formatter.JSONFormatter)
    - mono (monochrome)
    - linux_interactive, linux_production (vga console)


.. note::

    When there are conflicting arguments to the ``configure`` method,
    the last specified will win.
    This requires a Python version >=3.6, due to ordered keyword args.
    Below this version it is not recommended to try since keyword order
    will be undefined and therefore the result.
    One workaround, call ``configure()`` twice.


Syntax Highlighting w/Pygments
--------------------------------

When Pygments is installed,
syntax highlighting is available for Python data structures and code,
as well as JSON and XML strings—\
potentially anything Pygments can highlight.
This can be helpful when debugging remote APIs for example.

A lexer may be
`selected by name <http://pygments.org/docs/lexers/>`_
via ``configure(lexer=LEXER_NAME)``,
disabled by setting to ``None``.
Some common lexer names are: ``('json', 'python3', 'xml')``.

**Use:**

Message text following a ``{, [, <, or '`` char
is highlighted with the current
lexer+formatter:

.. code-block:: python

    out.configure(level='trace')

    # default Python3
    out.trace('PYON data: %s',
              {'data': [None, True, False, 123]})

    out.configure(lexer='json')
    out.trace('JSON data: '
              '{"data": [null, true, false, 123]}')

(Imagine with lovely ANSI flavors. 😁)


Performance
-----------------

out does quite a few things,
but it tries not to do any duplicate work or anything excessively stupid.
It takes about 25 microseconds to log a simple message,
or ~90 for a complex highlighted one on a newer machine.
Had to run a loop several thousand times (only logging) before it added up to
a noticeable delay.

Theming and highlighting are easy to turn off for production mode,
so "out" should hopefully not slow you down at all when not developing.


Tips
---------

- By default the logger prints to ``stderr``.
  The reason being that when used in an interactive script normal application
  output may be easily segregated from log messages during redirection.

  .. code-block:: shell

    # bash, fish
    ⏵ script.py 2> logfile.txt

  Configurable via the ``stream`` keyword to ``.configure()``:

  .. code-block:: python

      import sys, out

      out.configure(
          stream=sys.stdout,
      )

- Upgrading a long script from ``print()`` is easy:

  .. code-block:: python

    import out

    print = out  # or other level: out.note

  Or perhaps some logging was already added, but you'd like to downsize.
  Add this to your main script::

    import out as logger

  Less code will need to be changed.

.. ~ - Want to keep your complex configuration but use the ``ColorFormatter`` class
  .. ~ and themes in your own project?

- The ``ColorFormatter`` and ``JSONFormatter`` classes can be used in your own
  project:

  .. code-block:: python-console

    >>> from out.format import ColorFormatter

    >>> cf = ColorFormatter()
    >>> handler.setFormatter(cf)

- To print the current logging configuration:

  .. code-block:: python-console

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
also known as the "root" logger.


Troubleshooting
-----------------

- If you'd like to know what ``out`` is doing,
  try running the ``.log_config()`` method to log what's currently up:

  .. code-block:: python-console

      >>> out.log_config()

  .. code-block:: shell

      🅳   out logging config, version: '0.70a1'
      🅳     .name: main, id: 0x7f88e9ec7198
      🅳     .level: debug (10)
      🅳     .default_level: info (20)
      🅳     + Handler: 0 <StreamHandler <stdout> (NOTSET)>
      🅳       + Formatter: <out.format.ColorFormatter object at 0x7f88e9ce1b70>
      🅳         .datefmt: '%H:%M:%S'
      🅳         .msgfmt: '  {on}{icon:<2}{off} \x1b[38;5;242m{name}/\x1b[38;5;245m{funcName}:\x1b[32m{lineno:<3}\x1b[0m {message}'
      🅳         fmt_style: <logging.StrFormatStyle object at 0x7f88e9ca5080>
      🅳         theme.styles: {'TRACE': '\x1b[35m', 'DEBUG': '\x1b[34m', 'INFO': '\x1b[32m', 'NOTE': '\x1b[96m', 'WARNING': '\x1b[93m', 'ERROR': '\x1b[31m', 'EXCEPT': '\x1b[91m', 'CRITICAL': '\x1b[97m', 'FATAL': '\x1b[97m', 'NOTSET': ''}
      🅳         theme.icons: {'TRACE': '🆃', 'DEBUG': '🅳', 'INFO': '🅸', 'NOTE': '🅽', 'WARNING': '🆆', 'ERROR': '🅴', 'EXCEPT': '🆇', 'CRITICAL': '🅵', 'FATAL': '🅵', 'NOTSET': '🅽'}
      🅳         highlighting: 'Python3Lexer', 'Terminal256Formatter'

  Import ``out`` in debug mode first and you can see any logging other modules do
  as the start up.

- If you're using fbterm, make sure the ``TERM`` environment variable is set
  to ``fbterm``.
  This makes several adjustments to help it work better under that terminal.


Install
------------

.. code-block:: shell

    ⏵ pip3 install out  # or out[highlight]
