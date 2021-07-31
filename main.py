import os
import zipfile
from config import Config
from watchdog_handler import WatchdogHandler


def zipdir(path: str, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


if __name__ == '__main__':
    # zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    # zipdir('test/', zipf)
    # zipf.close()
    conf = Config()  # TODO: make global
    conf.load_config()
    conf.config["paths"].append("test")  # TODO debbuging
    WatchdogHandler(conf.config).start_handler()
