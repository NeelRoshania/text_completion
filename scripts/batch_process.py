import argparse
from datetime import datetime
import uuid
import logging
import logging.config

from chatgpt_poc import app
from chatgpt_poc.csv import write_csv, read_csv
from chatgpt_poc.tasks import completion_task, await_tasks_completion

from multiprocessing.dummy import Pool
from kombu.exceptions import OperationalError

# logging configurations
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': f'logs/{__name__}.log'})
LOGGER = logging.getLogger(__name__)

"""

    References
        - https://platform.openai.com/docs/api-reference/introduction?lang=python

"""

# tasks

def retry_tasks(job_id: str, prompts: str) -> None:

    """
        Submitting predefined tasks with retry logic if failed
        
    """

    tasks = []

    try:

        # generate tasks
        for prompt in enumerate(prompts):
            tasks.append(
                [
                    datetime.utcnow().isoformat(),
                    completion_task.apply_async(args=[prompt[1]], queue='chatgpt_poc_queue').id
                ]
            )
            # break

        LOGGER.info(f'{job_id} - tasks submitted')

        return tasks

    except OperationalError as e: 
        LOGGER.error(f'app:{app} - failed to execute tasks - {e}')

# jobs

def job_handler(job_id: str, prompts_loc:str) -> tuple:

    """
        Submit jobs of predefined tasks

    """
    try:
        LOGGER.info(f'{job_id} - starting job')
        
        # submit tasks
        header, *titles = read_csv(prompts_loc)
        tasks_submitted = retry_tasks(job_id=job_id, prompts=[title[0] for title in titles])
        taskids = [task[1] for task in tasks_submitted]
        write_csv(file_loc=f'data/results/jobs/submitted/{job_id}.csv', data=list(tasks_submitted)) # [date_started, task_id]
        
        # check for results - not really the best way to track this
        res = await_tasks_completion(taskids=taskids) # blocking
        write_csv(file_loc=f'data/results/jobs/completed/{job_id}.csv', data=list(res))  # [taskid, state, date_done, result]

    except OperationalError as e: 
        LOGGER.error(f'app:{app} - failed to execute tasks - {e}')

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('titles', type=str, action="store", help='csv file of titles for completion')
    # parser.add_argument("--optional", "-o", action="store", type=str, default=8000)
    args = parser.parse_args()

    # submit titles for completion
    job_handler(job_id=str(uuid.uuid1()), prompts_loc=args.titles)
