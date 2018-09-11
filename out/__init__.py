'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.
'''
import sys
import logging
import traceback

from console.detection import is_a_tty

from .format import ColorFormatter
from .themes import theme_maps as _theme_maps


_out_file = sys.stderr
_is_a_tty = is_a_tty(_out_file)

# Allow string as well as constant access, more levels are added below:
level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'warning': logging.WARN,
    'err': logging.ERROR,
    'error': logging.ERROR,
    'critical': logging.FATAL,
    'fatal': logging.FATAL,
}


class Logger(logging.Logger):
    '''
        Singleton logger.
    '''
    default_level = logging.INFO

    def configure(self, **kwargs):
        ''' Convenience function to set a number of parameters on this logger
            and associated handlers and formatters.
        '''
        for kwarg in kwargs:
            value = kwargs[kwarg]

            if kwarg == 'level':
                self.set_level(value)

            elif kwarg == 'default_level':
                self.default_level = level_map.get(value, value)

            elif kwarg == 'datefmt':
                self.handlers[0].formatter.datefmt = value

            elif kwarg == 'msgfmt':
                self.handlers[0].formatter._style._fmt = value

            elif kwarg == 'stream':
                self.handlers[0].stream = value

            else:
                setattr(self, kwarg, value)

    def log_config(self):
        ''' Log the current configuration. '''
        level = self.level
        self.debug('Logging config:')
        self.debug('/ name: {}, id: {}', self.name, id(self))
        self.debug('  .level: %s (%s)', level_map_int[level], level)
        self.debug('  .default_level: %s', self.default_level)
        for i, handler in enumerate(self.handlers):
            fmtr = handler.formatter
            self.debug('  + Handler: %s %r', i, handler)
            self.debug('    + Formatter: %r', fmtr)
            self.debug('      .style: %r', fmtr._style)
            self.debug('      .datefmt: %r', fmtr.datefmt)
            self.debug('      .msgfmt: {!r}', fmtr._fmt)

    def setLevel(self, level):

        if type(level) is int:
            super().setLevel(level)
        else:
            self.setLevel(level_map.get(level, level))
    set_level = setLevel

    def __call__(self, message, *args):
        if self.isEnabledFor(self.default_level):
            self._log(self.default_level, message, args)


def add_logging_level(name, value, method_name=None):
    ''' Comprehensively adds a new logging level to the ``logging`` module and
        the currently configured logging class.

        Derived from: https://stackoverflow.com/a/35804945/450917
    '''
    if not method_name:
        method_name = name.lower()

    # set levels
    logging.addLevelName(value, name)
    setattr(logging, name, value)
    level_map[name.lower()] = value

    if value == getattr(logging, 'EXCEPT', None):  # needs traceback added
        def logForLevel(self, message='', *args, **kwargs):
            if self.isEnabledFor(value):
                message = (message + ' ▾\n').lstrip() + traceback.format_exc()
                self._log(value, message, args, **kwargs)
    else:
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(value):
                self._log(value, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):  # may not need
        logging.log(value, message, *args, **kwargs)

    # set functions
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


# re-configure root logger
out = logging.getLogger()   # root
out.__class__ = Logger      # one way to add call()

# odd level numbers chosen to avoid commonly configured variations
add_logging_level('TRACE', 7)
add_logging_level('NOTE', 27)
add_logging_level('EXCEPT', logging.ERROR + 3, 'exc')
add_logging_level('FATAL', logging.FATAL)
level_map_int = {
    val: key
    for key, val in level_map.items()
}
out.warn = out.warning  # fix warn
out.setLevel('info')  # lowered to info - note didn't show up by default.


# handler/formatter
_handler = logging.StreamHandler(stream=_out_file)
_theme = _theme_maps['interactive' if _is_a_tty else 'production']
_formatter = ColorFormatter(tty=_is_a_tty, **_theme)
_formatter.default_msec_format = '%s.%03d'
_handler.setFormatter(_formatter)
out.addHandler(_handler)

# save original module for later, in case it's needed.
out._module = sys.modules[__name__]

# Wrap module with instance for direct access
sys.modules[__name__] = out
