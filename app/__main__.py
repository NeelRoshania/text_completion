import argparse
import subprocess
import logging

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    # parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?") # need to define this
    parser.add_argument("--concurrency", "-c", default=1)
    args = parser.parse_args()

    LOGGER = logging.getLogger(__name__)

    # run celery worker as a subprocess
    LOGGER.info(f'starting celery worker node - concurrency: {args.concurrency}')
    subprocess.Popen(
                        [
                            "celery",
                            "-A",
                            "chatgpt_poc",
                            "worker",
                            "-Q",
                            "chatgpt_poc_queue",
                            "--loglevel=INFO",
                           f'--concurrency={args.concurrency}',
                            # "--logfile=logs/celery.log"
                            ]
    )

