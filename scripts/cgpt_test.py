import argparse
import logging
import logging.config

from chatgpt_poc.csv import write_csv
from chatgpt_poc.text_completion import request_completion
import uuid
from multiprocessing.dummy import Pool

# logging configurations
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': f'logs/{__name__}.log'})
LOGGER = logging.getLogger(__name__)

"""

    References
        - https://platform.openai.com/docs/api-reference/introduction?lang=python

"""

if __name__ == "__main__":

    LOGGER.info('starting app')

    prompts = ["How are you?", "What is your name?", "What is the meaning of life?"]

    with Pool() as pool:
        results = pool.map(request_completion, prompts)

    write_csv(
        file_loc=f'tests/data/responses/{str(uuid.uuid1())}.csv', 
        data=list(zip(prompts, results)), 
        schema=['prompt', 'response']
        )

    LOGGER.info('app complete') 

