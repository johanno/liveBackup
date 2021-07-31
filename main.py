import os
import zipfile
from config import Config
from watchdog_handler import WatchdogHandler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def zipdir(path: str, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
def print_log(handler: WatchdogHandler):
    pass  #TODO implement backup logic...

if __name__ == '__main__':
    # zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    # zipdir('test/', zipf)
    # zipf.close()
    conf = Config()  # TODO: make global
    conf.load_config()
    conf.config["paths"].append("test")  # TODO debbuging
    wd_handler = WatchdogHandler(conf.config)
    wd_handler.start_handler()

    sched = BlockingScheduler()

    # TOOD: change time and probably get it from config
    sched.add_job(print_log, trigger=CronTrigger(second=10), args=[wd_handler])
    sched.start()
