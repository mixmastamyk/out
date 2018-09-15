import out

import test_mod; test_mod  # pyflakes
print('-' * 50)

#~ ltd = out
#~ while ltd is not None:
    #~ print(f'  logger: {ltd.name}, level:{ltd.level}, id:{id(ltd)}, {ltd.handlers}')
    #~ ltd = ltd.parent


def test_it(full=True):

    out('no explicit level')
    out.trace('trace msg: %s', 'Absurdly voluminous details…')
    out.debug('debug message')
    out.info('info message - Normal feedback')
    out.note('note message - Important positive feedback to remember.')
    out.warn('warn message - Something to worry about.')

    if full:
        try:
            1/0
        except Exception as err:
            out.error('error message - Pow!')
            out.exception('exception message - Kerblooey!')
            out.exc('exc message - Kerblooey!')
            out.exc()

        out.critical('critical message - *flatline*')
        out.fatal('fatal message - *flatline*')
    print('-' * 50)


print()
out.configure(
    level='trace',
    lexer='json',
)
out.debug('debug message: JSON:\t{"data": [null, true, false, 123]}')

out.configure(lexer='xml')
out.trace('debug message: XML:\t<foo><bar attr="woot">baz</bar></foo>')


out.configure(lexer='python3')
out.note('debug message: PyON:\t%r', {'data': [None, True, False, 123]})
test_it()

out.log_config()

out.configure(
    style='mono',
    msgfmt='{asctime}.{msecs:03.0f} {on}{levelname:<7} '
            '{name}/{funcName}:{lineno} {message} {off}',
)
test_it()

print('Set to plain theme, with std formatter for modest speed boost:\n')
out.configure(
    theme='plain',
    #~ theme='json',
)
out('no explicit level')
out.trace('trace msg: %s', 'Absurdly voluminous details…')
out.debug('debug message')

#~ print('With msgfmt configured:')
#~ print()
#~ out.configure(msgfmt='{asctime} {name} {message}')
#~ test_it(False)

#~ print('=========== APP OUTPUT ===========')
#~ print('=========== APP OUTPUT ===========')


