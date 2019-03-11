import time
import logging
from functools import wraps
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

logger = RamaLogger().getLogger()

def retry(ExceptionToCheck, logger=logger, reconnect_when_error=False):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            total_tries = Config.getint('Retry_When_Error', 'Retry_Times')
            mtries = total_tries
            mdelay = Config.getint('Retry_When_Error', 'Retry_Delay_Ms') / 1000
            backoff = Config.getint('Retry_When_Error', 'Backoff')
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %.1f seconds (%d / %d)..." % (str(e), mdelay, total_tries - mtries + 1, total_tries)
                    logger.warning(msg)
                    if reconnect_when_error:
                        args[0].Connect()
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry