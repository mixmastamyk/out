import logging

#~ import out as log
log = logging.getLogger(__name__)


#~ print('  during mod: logging.root: %s', id(logging.root))
#~ ltd = log
#~ while ltd is not None:
    #~ print(f'  logger: {ltd.name}, level:{ltd.level}, id:{id(ltd)}, {ltd.handlers}')
    #~ ltd = ltd.parent

log.debug('debug text from module')
log.info('info text from module')
log.warn('warning text from module')
log.fatal('fatal text from module')
