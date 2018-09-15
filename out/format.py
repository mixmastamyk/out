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

from .highlight import (highlight as _highlight, term_formatter,
                        get_lexer_by_name)
import out.themes as _themes

_end = str(fx.end)
DATA_SEARCH_INTERVAL = (0, 80)


class ColorFormatter(logging.Formatter):
    ''' Colors the level-name of a log message according to the level.

        Arguments:

            datefmt         - strftime datetime template
            fmt             - log template
            icons           - dict of level:value for icons
            style           - dict of level:value for terminal style
            template_style  - log template syntax: %, {, $
            tty             - if in a tty, to toggle escape sequences

            # highlighting
            lexer           - None, or Pygment's lexer: python3', 'json', etc.
            code_indent     - If highlighting data containing newlines, indent.
    '''
    default_msec_format = '%s.%03d'  # use period decimal point

    def __init__(self,
                 datefmt=None,
                 fmt=None,
                 icons=None,
                 style=None,
                 template_style='{',
                 tty=True,
                 lexer='python3',
                 code_indent=12,
        ):
        self._theme_style = style if style else _themes.styles['norm']
        self._theme_icons = icons if icons else _themes.icons['rounded']
        self._code_indent = code_indent
        #~ self._is_a_tty = tty
        self._highlight = self._lexer = None
        if tty and lexer:
            self._highlight = _highlight
            self.set_lexer(lexer)

        super().__init__(fmt=fmt, datefmt=datefmt, style=template_style)

    def set_lexer(self, name):
        self._lexer = get_lexer_by_name(name)
        self._lexer.ensurenl = False

    def format(self, record):
        ''' Log color formatting. '''
        levelname = record.levelname    # len7 limit
        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        # render the message part with arguments
        try:  # Allow {} style - need a faster way to determine this:
            message = record.getMessage()
        except TypeError:
            message = record.msg.format(*record.args)

        # decide to highlight w/ pygments
        if self._highlight:
            pos = message.find('\t', *DATA_SEARCH_INTERVAL)
            if pos != -1:
                front, back = message[:pos], message[pos+1:]  # Spliten-Sie
                back = self._highlight(back, self._lexer, term_formatter)
                if front.endswith('\n'):                    # indent data?
                    back = left_indent(back, self._code_indent) + '\n'
                message = front + ' ' + back  # f'{front} {back}'

        record.message = message
        record.on = self._theme_style.get(levelname, '')
        record.icon = self._theme_icons.get(levelname, '')
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


class JSONFormatter(logging.Formatter):
    '''
        Formats a log message into line-oriented JSON.

        The message template format is different.
        It uses simple CSV (no spaces allowed) to define field order, e.g.:

            fmt='asctime,msecs,levelname,name,funcName,lineno,message'

        (Currently field order requires Python 3.6, but could be backported.)
    '''
    def __init__(self, datefmt=None, fmt=None):
        self._fields = fmt.split(',')
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        ''' Log color formatting. '''
        levelname = record.levelname
        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'
        record.asctime = self.formatTime(record, self.datefmt)

        # render the message part with arguments
        try:  # Allow {} style - need a faster way to determine this:
            message = record.getMessage()
        except TypeError:
            message = record.msg.format(*record.args)
        record.message = message

        fields = self._fields
        data = { name: getattr(record, name) for name in fields }
        if 'asctime' in data and 'msecs' in data:  # needs option for this
            data['asctime'] += '.{:03.0f}'.format(data.pop('msecs'))
        s = repr(data)

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
