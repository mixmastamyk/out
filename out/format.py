'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    Message template variables:

        {name}              Name of the logger (logging channel)
        {levelno}           Numeric logging level for the message (DEBUG, INFO,
                                WARNING, ERROR, CRITICAL)
        {levelname}         Text logging level for the message ("DEBUG", "INFO",
                                "WARNING", "ERROR", "CRITICAL")
        {pathname}          Full pathname of the source file where the logging
                                call was issued (if available)
        {filename}          Filename portion of pathname
        {module}            Module (name portion of filename)
        {lineno)d           Source line number where the logging call was issued
                                (if available)
        {funcName}          Function name
        {created}           Time when the LogRecord was created (time.time()
                                return value)
        {asctime}           Textual time when the LogRecord was created
        {msecs}             Millisecond portion of the creation time
        {relativeCreated}   Time in milliseconds when the LogRecord was created,
                            relative to the time the logging module was loaded
                            (typically at application startup time)
        {thread}            Thread ID (if available)
        {threadName}        Thread name (if available)
        {process}           Process ID (if available)
        {message}           The result of record.getMessage(), computed just as
                                the record is emitted

        # added:
        {color}{icon}{off}  Color and icon support.


    TODO:

        'format': ' %(levelname)-7.7s %(name)s/%(funcName)s:%(lineno)s'
                  ' %(message)s'

        'format': '  %(icon)s %(levelname)-7.7s[0m ' # %(levelno)s
                  '[38;5;242m%(name)s/'
                  '[38;5;245m%(funcName)s:'
                  '[32m%(lineno)s[0m'
                  ' %(message)s',
'''
import logging

from console.style import fx

from .highlight import pygments, highlight, lex, fmt
from .themes import color_maps, icon_maps


_end = str(fx.end)
DATA_SEARCH = (0, 60)


class ColorFormatter(logging.Formatter):
    ''' Colors the level-name of a log message according to the level.

    '''
    def __init__(self,
                 color_map=None,
                 datefmt=None,
                 fmt=None,
                 highlight=True,
                 icon_map=None,
                 template_style='{',
                 tty=True,
                ):
        self._is_a_tty = tty
        self.color_map = color_map if color_map else color_maps['norm']
        self.icon_map = icon_map if icon_map else icon_maps['rounded']

        super().__init__(fmt=fmt, datefmt=datefmt, style=template_style)

    def format(self, record):
        ''' Log color formatting, probably could be done better. '''
        levelname = record.levelname    # len7 limit
        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message = record.getMessage()  # renders msg part with args

        # decide to highlight w/ pygments
        if pygments and self._is_a_tty:
            for datachar in ('{', '['):
                pos = message.find(datachar, *DATA_SEARCH)
                if pos != -1:
                    front, back = message[:pos], message[pos:]  # Spliten-Sie
                    back = highlight(back, lex, fmt)
                    if front.endswith('\n'):                    # indent data?
                        back = left_indent(back)

                    message = front + back
                    break  # once thanks

        record.message = message
        record.color = self.color_map.get(levelname, '')
        record.icon = self.icon_map.get(levelname, '')
        record.off = _end
        s = self.formatMessage(record)

        # this needs to be here, Formatter class isn't very extensible.
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


def left_indent(text, indent=12):
    ''' A bit of the ol' ultraviolence  :-/ '''
    indent=' ' * indent
    return ''.join((indent + line for line in text.splitlines(True)))
