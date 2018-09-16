'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    This module contains themes for colors, icons, message and date formats.
    They can be used separately, or together as a "full" theme.
'''
from console import fg, fx


icons = dict(

    symbol = dict(
        TRACE    = '• ',
        DEBUG    = '• ',
        INFO     = '✓ ',
        NOTE     = '🎗 ',
        WARNING  = '⚠ ',
        ERROR    = '✗ ',
        EXCEPT   = '💣',
        CRITICAL = '💀',
        FATAL    = '💀',
        NOTSET   = '␀ ',
    ),
    circled_lower = dict(
        TRACE    = 'ⓣ ',
        DEBUG    = 'ⓓ ',
        INFO     = 'ⓘ ',
        NOTE     = 'ⓝ ',
        WARNING  = 'ⓦ ',
        ERROR    = 'ⓔ ',
        EXCEPT   = 'ⓧ ',
        CRITICAL = 'ⓕ ',
        FATAL    = 'ⓕ ',
        NOTSET   = 'ⓝ ',
    ),
    ascii = dict(
        TRACE    = 'T ',
        DEBUG    = 'D ',
        INFO     = 'I ',
        NOTE     = 'N ',
        WARNING  = 'W ',
        ERROR    = 'E ',
        EXCEPT   = 'X ',
        CRITICAL = 'F ',
        FATAL    = 'F ',
        NOTSET   = 'N ',
    ),
    ascii_symbol = dict(
        TRACE    = '~ ',
        DEBUG    = '- ',
        INFO     = '= ',
        NOTE     = '> ',
        WARNING  = '! ',
        ERROR    = '! ',
        EXCEPT   = '! ',
        CRITICAL = '!!',
        FATAL    = '!!',
        NOTSET   = '_ ',
    ),
    circled = dict(
        TRACE    = '🅣 ',
        DEBUG    = '🅓 ',
        INFO     = '🅘 ',
        NOTE     = '🅝 ',
        WARNING  = '🅦 ',
        ERROR    = '🅔 ',
        EXCEPT   = '🅧 ',
        CRITICAL = '🅕 ',
        FATAL    = '🅕 ',
        NOTSET   = '🅝 ',
    ),
    rounded = dict(
        TRACE    = '🆃 ',
        DEBUG    = '🅳 ',
        INFO     = '🅸 ',
        NOTE     = '🅽 ',
        WARNING  = '🆆 ',
        ERROR    = '🅴 ',
        EXCEPT   = '🆇 ',
        CRITICAL = '🅵 ',
        FATAL    = '🅵 ',
        NOTSET   = '🅽 ',
    ),
)

_fatal_clr = fg.lightwhite

styles = dict(
    norm = dict(
        TRACE    = str(fg.purple),
        DEBUG    = str(fg.blue),
        INFO     = str(fg.green),
        NOTE     = str(fg.lightcyan),
        WARNING  = str(fg.lightyellow),
        ERROR    = str(fg.red),
        EXCEPT   = str(fg.lightred),
        CRITICAL = str(_fatal_clr),
        FATAL    = str(_fatal_clr),
        NOTSET   = '',
    ),
    bold = dict(
        TRACE    = str(fg.purple),
        DEBUG    = str(fg.blue),
        INFO     = str(fg.lightgreen),
        NOTE     = str(fg.cyan + fx.bold),
        WARNING  = str(fg.yellow + fx.bold),
        ERROR    = str(fg.red + fx.bold),
        EXCEPT   = str(fg.lightred + fx.bold),
        CRITICAL = str(_fatal_clr + fx.bold),
        FATAL    = str(_fatal_clr + fx.bold),
        NOTSET   = '',
    ),
    mono = dict(
        TRACE    = str(fx.dim),
        DEBUG    = str(fx.dim),
        INFO     = '',
        NOTE     = str(fx.italic),
        WARNING  = str(fx.italic),
        ERROR    = str(fx.bold),
        EXCEPT   = str(fx.bold),
        CRITICAL = str(fx.bold + fx.reverse),
        FATAL    = str(fx.bold + fx.reverse),
        NOTSET   = '',
    ),
)
_blink = styles['norm'].copy()
_blink['FATAL'] = str(_fatal_clr + fx.blink)
styles['blink'] = _blink


# these are full themes, colors, icons, msg and date formats
themes = dict(
    interactive = dict(
        style = styles['norm'],
        icons = icons['rounded'],
        fmt='  {on}{icon:<2}{off} ' +
            fg.i242 + '{name}/' +  # dark grey
            fg.i245 + '{funcName}:' +  # medium grey
            fg.green + '{lineno:<3}' + fx.end +
            ' {message}',
        datefmt='%H:%M:%S',
    ),

    production = dict(
        style = None,
        icons = icons['symbol'],
        fmt='{asctime}.{msecs:03.0f} {on}{icon:<2} {levelname:<7}{off} '
            '{name}/{funcName}:{lineno} {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
    ),

    plain = dict(
        fmt='{asctime}.{msecs:03.0f} {levelname:<7} {name}/{funcName}:{lineno}'
            ' {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
    ),

    json = dict(
        fmt='asctime,msecs,levelname,name,funcName,lineno,message',
        datefmt='%Y-%m-%d %H:%M:%S',
    ),

    mono = dict(
        datefmt='%Y-%m-%d %H:%M:%S',
        style='mono',
        fmt='{asctime}.{msecs:03.0f} {on}{levelname:<7} '
            '{name}/{funcName}:{lineno} {message}{off}',
    ),

    linux_interactive = dict(
        style = styles['norm'],
        icons = icons['ascii'],
        fmt='  {on}{levelname:<7}{off} ' +
            fg.lightblack + '{name}/{funcName}:' +  # dark grey
            fg.green + '{lineno:<3}' + fx.end +
            ' {message}',
    ),
    linux_production = dict(
        style = styles['norm'],
        icons = None,
        fmt='{asctime}.{msecs:03.0f} {on}{levelname:<7}{off} '
            '{name}/{funcName}:{lineno} {message}',
    ),

)
