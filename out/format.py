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
        {on}…{off}          Toggles level-specific style (colors, etc) support.
        {icon}              Level-specific icon.
'''
import logging

from console.style import fx

from .highlight import pygments, highlight, lex, fmt
import out.themes as _themes


_end = str(fx.end)
DATA_SEARCH = (0, 60)


class ColorFormatter(logging.Formatter):
    ''' Colors the level-name of a log message according to the level.

    '''
    default_msec_format = '%s.%03d'  # use period decimal point

    def __init__(self,
                 fmt=None,
                 datefmt=None,
                 highlight=True,
                 icons=None,
                 style=None,
                 template_style='{',
                 tty=True,
                ):
        self._is_a_tty = tty
        self.style = style if style else _themes.style['norm']
        self.icons = icons if icons else _themes.icons['rounded']

        super().__init__(fmt=fmt, datefmt=datefmt, style=template_style)

    def format(self, record):
        ''' Log color formatting, probably could be done better. '''
        levelname = record.levelname    # len7 limit
        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        try:  # Allow {} style - need a faster way to determine this:
            message = record.getMessage()  # renders msg part with args
        except TypeError as err:
            message = record.msg.format(*record.args)

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
        record.on = self.style.get(levelname, '')
        record.icon = self.icons.get(levelname, '')
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
