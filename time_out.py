
# early attempt at profiling this
#~ python3 -m timeit -n 10000 "$(cat time_out.py)"
#~ 10000 loops, best of 5: 25.4 usec per loop

import out


#~ basic = True
basic = False

try:
    if basic:
        import cProfile

        with cProfile.Profile() as pr:

            for _ in range(10_000):
                out.trace('debug: {"text": "from main"}')
                out.debug('debug: {"text": "from main"}')
                out.info('info text')
                out.note('note text')
                out.warn('warn text')
                out.fatal('fatal text')

            pr.print_stats(sort='cumulative')

    else:
        out.configure(lexer='json')

        import cProfile

        with cProfile.Profile() as pr:

            for _ in range(10_000):
                out.debug(
                    'debug message: JSON: %s',
                    '{"data": [null, true, false, "hi", 123]}'
                )
                out.warn('warn: {"text": "from main"}')
                out.error(
                    'error message: JSON: %s',
                    '{"data": [null, true, false, "hi", 123]}'
                )

            pr.print_stats(sort='cumulative')

except BrokenPipeError as err:
    pass
