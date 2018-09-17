'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.
'''

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter

    from pygments.token import (Keyword, Name, Comment, String, Error,
                                Number, Operator, Generic, Token, Punctuation)

    # Pygments highlighting
    TERMINAL_COLORS = {     # light-bg      # dark-bg
        Token:              ('',            ''),

        Comment:            ('darkgray',    'darkgray'),
        Comment.Preproc:    ('teal',        'turquoise'),
        Keyword:            ('*darkblue*',   'blue'),
        Keyword.Type:       ('teal',        'turquoise'),
        Keyword.Constant:   ('teal',        'turquoise'),

        Operator.Word:      ('*darkblue*',   'blue'),
        #~ Operator:           ('brown',      'yellow'),  # 16 colors not very good
        #~ Punctuation:        ('brown',      'yellow'),

        Name.Builtin:       ('teal',        'turquoise'),
        Name.Builtin.Pseudo:('teal',        'turquoise'),

        #~ Name.Function:              ('',            ''),
        Name.Namespace:     ('',            ''),
        #~ Name.Class:               ('',            ''),
        Name.Exception:     ('teal',        'turquoise'),
        Name.Decorator:     ('fuchsia',     'purple'),
        Name.Variable:      ('darkred',     'red'),
        #~ Name.Attribute:     ('teal',        'turquoise'),
        Name.Tag:           ('darkblue',        'red'),
        #~ String:             ('red',       'darkred'),
        String:             ('purple',       'fuchsia'),
        Number:             ('green',       'darkgreen'),

        Generic.Deleted:    ('darkred',     'red'),
        Generic.Inserted:   ('darkgreen',   'green'),
        Generic.Heading:    ('**',          '**'),
        Generic.Subheading: ('*purple*',    '*fuchsia*'),
        Generic.Error:      ('red',         'red'),
        Error:              ('_red_',       '_red_'),
    }

    #~ term_formatter = TerminalFormatter(colorscheme=TERMINAL_COLORS)
    # temp 256 color support:
    from pygments.style import Style
    from pygments.formatters import Terminal256Formatter

    class AStyle(Style):
        styles = {
            Token.String:           '#b40',  # orange, amber
            Comment:                'italic #888',

            Keyword:                'bold #ansiblue',
            Keyword.Constant:       'nobold #ansiteal',
            Number:                 '#ansidarkgreen',

            Name.Tag:               'bold #b40',
            #~ Name.Tag:               '#3ac',
            #~ Name.Attribute:         'nobold #ca7',
            Name.Attribute:         'nobold #ansibrown',
            #~ Name:                   '#f00',
            #~ Name.Function:          '#0f0',
            #~ Name.Class:             'bold #0f0',
            #~ String:                 'bg:#eee #111'
            Punctuation:           'nobold #ca7',
            #~ Punctuation:        ('brown',      'yellow'),
        }

    term_formatter = Terminal256Formatter(style=AStyle)

except ImportError:
    highlight = term_formatter = get_lexer_by_name = None
