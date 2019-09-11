'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    Highlighting with Pygments!

    pygments_color_name_mapping = {  # old names --> new
        'darkred'    : 'red',
        'darkgreen'  : 'green',
        'brown'      : 'yellow',
        'darkblue'   : 'blue',
        'purple'     : 'magenta',
        'teal'       : 'cyan',
        'lightgray'  : 'gray',
        'darkgray'   : 'brightblack',
        'red'        : 'brightred',
        'green'      : 'brightgreen',
        'yellow'     : 'brightyellow',
        'blue'       : 'brightblue',
        'fuchsia'    : 'brightmagenta',
        'turquoise'  : 'brightcyan',
        'darkyellow' : 'yellow',
        'darkteal'   : 'brightcyan',
        'fuscia'     : 'brightmagenta',
    }

'''
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.token import (Keyword, Name, Comment, String, Error,
                                Number, Operator, Punctuation,
                                Token, Generic, Whitespace)
except ImportError:
    highlight = get_lexer_by_name = None


def get_term_formatter(_CHOSEN_PALETTE):
    ''' Build formatter according to environment. '''
    term_formatter = None

    if _CHOSEN_PALETTE and highlight:

        if _CHOSEN_PALETTE in ('extended', 'truecolor'):

            from pygments.formatters import Terminal256Formatter
            from pygments.style import Style

            class OutStyle(Style):
                styles = {
                    Comment:                'italic ansibrightblack',
                    Keyword:                'bold #4ac',  # light blue
                    Keyword.Constant:       'nobold ansicyan',
                    Number:                 'ansigreen',

                    Name.Tag:               '#4ac',  # light blue, xml, json
                    Name.Attribute:         '#4ac',  # light blue

                    Operator:               'nobold #b94',
                    Operator.Word:          'bold #4ac',
                    Punctuation:            'nobold #b94',

                    String:                 'ansibrightmagenta',  # amber
                    Generic.String:         'ansired',
                }
            term_formatter = Terminal256Formatter(style=OutStyle)

        elif _CHOSEN_PALETTE == 'basic':

            from pygments.formatters import TerminalFormatter

            _default = ('', '')
            _TERMINAL_COLORS = {
                Comment.Preproc:    _default,
                Name:               _default,
                Token:              _default,
                Whitespace:         _default,
                Generic.Heading:    ('**',                  '**'),

                Comment:            ('brightblack',         'brightblack'),
                Keyword:            ('*brightblue*',        '*brightblue*'),
                Keyword.Constant:   ('cyan',                'cyan'),
                Keyword.Type:       ('cyan',                'cyan'),
                Operator:           ('yellow',              'yellow'),
                Operator.Word:      ('*brightblue*',        '*brightblue*'),

                Name.Builtin:       ('cyan',                'cyan'),
                Name.Decorator:     ('magenta',             'magenta'),
                Name.Tag:           ('brightblue',          'brightblue'),
                Name.Attribute:     ('brightblue',          'brightblue'),

                String:             ('brightmagenta',       'brightmagenta'),
                Number:             ('green',               'green'),

                Generic.Deleted:    ('red',                 'brightred'),
                Generic.Inserted:   ('green',               'brightgreen'),
                Generic.Error:      ('brightred',           'brightred'),

                Error:              ('_brightred_',         '_brightred_'),
            }

            term_formatter = TerminalFormatter(
                bg='dark',
                colorscheme=_TERMINAL_COLORS,
            )

    return term_formatter
