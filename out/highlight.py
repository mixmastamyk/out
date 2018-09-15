'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.
'''

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter
    #~ from pygments.formatters import Terminal256Formatter

    from pygments.token import (Keyword, Name, Comment, String, Error,
                                Number, Operator, Generic, Token,
                                #~ Punctuation,
                                )

    # Pygments highlighting
    TERMINAL_COLORS = {
        Token:              ('',            ''),

        Comment:            ('black',       'darkgray'),
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
        Name.Namespace:     ('',      ''),
        #~ Name.Class:               ('',            ''),
        Name.Exception:     ('teal',        'turquoise'),
        Name.Decorator:     ('fuchsia',     'purple'),
        Name.Variable:      ('darkred',     'red'),
        #~ Name.Attribute:     ('teal',        'turquoise'),
        Name.Tag:           ('darkblue',        'red'),
        #~ String:             ('darkred',       'darkred'),
        String:             ('purple',       'fuchsia'),
        Number:             ('darkgreen',   'darkgreen'),

        Generic.Deleted:    ('red',        'red'),
        Generic.Inserted:   ('darkgreen',  'green'),
        Generic.Heading:    ('**',         '**'),
        Generic.Subheading: ('*purple*',   '*fuchsia*'),
        Generic.Error:      ('red',        'red'),
        Error:              ('_red_',      '_red_'),
    }

    term_formatter = TerminalFormatter(colorscheme=TERMINAL_COLORS)

except ImportError:
    highlight = term_formatter = get_lexer_by_name = None
