import json
import os


class Config:
    def __init__(self):
        self.config_path: str = os.path.expanduser("~/.config/liveBackup.json")
        self.config: json = json.loads("""{
            "pattern": ["*"],
            "ignore_pattern": null,
            "paths": []
        }""")

    def load_config(self):
        if os.path.isfile(self.config_path):
            with open(self.config_path, "r") as fp:
                self.config = json.load(fp)
        else:
            with open(self.config_path, "w") as fp:
                json.dump(self.config, fp, indent=2)

    def save_config(self):
        with open(self.config_path, "w") as fp:
            json.dump(self.config, fp)


