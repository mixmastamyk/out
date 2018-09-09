'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    This module contains themes for colors, icons, message and date formats.
    They can be used separately, or together as a "full" theme.
'''
from console import fg, fx


icon_maps = dict(

    symbol = dict(
        TRACE    = '• ',
        DEBUG    = '• ',
        INFO     = '✓ ',
        WARNING  = '⚠ ',
        NOTE     = '🎗 ',
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
        WARNING  = 'ⓦ ',
        NOTE     = 'ⓝ ',
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
        WARNING  = 'W ',
        NOTE     = 'N ',
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
        WARNING  = '! ',
        NOTE     = '> ',
        ERROR    = '! ',
        EXCEPT   = '! ',
        CRITICAL = '!!',
        FATAL    = '!!',
        NOTSET   = '_',
    ),
    circled = dict(
        TRACE    = '🅣 ',
        DEBUG    = '🅓 ',
        INFO     = '🅘 ',
        WARNING  = '🅦 ',
        NOTE     = '🅝 ',
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
        WARNING  = '🆆 ',
        NOTE     = '🅽 ',
        ERROR    = '🅴 ',
        EXCEPT   = '🆇 ',
        CRITICAL = '🅵 ',
        FATAL    = '🅵 ',
        NOTSET   = '🅽 ',
    ),
)

_fatal_clr = fg.lightwhite

color_maps = dict(
    norm = dict(
        TRACE    = str(fg.purple),
        DEBUG    = str(fg.blue),
        INFO     = str(fg.green),
        WARNING  = str(fg.lightyellow),
        NOTE     = str(fg.lightcyan),
        ERROR    = str(fg.red),
        EXCEPT   = str(fg.lightred),
        CRITICAL = str(_fatal_clr),
        FATAL    = str(_fatal_clr),
        NOTSET   = str(fx.end),
    ),
    bold = dict(
        TRACE    = str(fg.purple),
        DEBUG    = str(fg.blue),
        INFO     = str(fg.lightgreen),
        WARNING  = str(fg.yellow + fx.bold),
        NOTE     = str(fg.cyan + fx.bold),
        ERROR    = str(fg.red + fx.bold),
        EXCEPT   = str(fg.lightred + fx.bold),
        CRITICAL = str(_fatal_clr + fx.bold),
        FATAL    = str(_fatal_clr + fx.bold),
        NOTSET   = str(fx.end),
    )
)

# these are full themes, colors, icons, msg and date formats
theme_maps = dict(
    interactive = dict(
        color_map = color_maps['norm'],
        icon_map = icon_maps['rounded'],
        fmt='  {color}{icon}{off} {message}',
        datefmt='%H:%M:%S',
    ),

    production = dict(
        color_map = None,
        icon_map = icon_maps['symbol'],
        fmt='{asctime} {color}{icon}{off}{levelname:<7} {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
)
