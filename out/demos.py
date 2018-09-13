import out

import test_mod; test_mod # pyflakes

#~ ltd = out
#~ while ltd is not None:
    #~ print(f'  logger: {ltd.name}, level:{ltd.level}, id:{id(ltd)}, {ltd.handlers}')
    #~ ltd = ltd.parent

def test_it(full=True):

    out('no explicit level')
    out.trace('trace msg: %s', 'Absurdly voluminous details…')
    out.debug('debug message: %s', {'data': [None, True, False, 123]})
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

#~ print('defaults:')
#~ print()
#~ full_test()


#~ print('With level TRACE:')
print()
out.configure(level='trace')
test_it()

out.log_config()

#~ print('With msgfmt configured:')
#~ print()
#~ out.configure(msgfmt='{asctime} {name} {message}')
#~ test_it(False)

#~ print('=========== APP OUTPUT ===========')
#~ print('=========== APP OUTPUT ===========')

