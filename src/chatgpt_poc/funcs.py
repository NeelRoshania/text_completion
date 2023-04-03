import datetime as dt
import logging
import random

from chatgpt_poc.csv import write_csv
from chatgpt_poc import cparser

LOGGER = logging.getLogger(__name__) # this calls the celery_template.funcs logger - which logs to worker node instance

def get_duration(start_time, end_time) -> float:

    """
        Calculate duration in seconds
        start_time:  time in seconds since the epoch as a floating point number
        end_time:  time in seconds since the epoch as a floating point number
    """
    return f'{end_time-start_time:.2f}'

def exponential_backoff(n0:int, retries: int) -> dt.datetime:

    """
        seconds to retrying the next task
            - exponential backoff + jitter
            - https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    """
    # temp = min(int(cparser["openai"]["ratelimitdelay"]), n0**(2*retries))
    # return sum([temp/2, random.uniform(0, temp/2)])

    temp = random.uniform(int(cparser["openai"]["ratelimitdelay"]), int(cparser["openai"]["ratelimit"])**(retries))
    return sum([temp, random.uniform(0, temp/2)])
