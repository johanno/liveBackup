from datetime import datetime
from typing import Union
from watchdog.observers import Observer
from watchdog.events import *
import json
from os.path import abspath, join


class WatchdogHandler:
    def __init__(self, config: dict):
        self.config = config
        self.file_log = {}
        self.log_path = "test.json"  #os.path.expanduser("~/.config/liveBackup.log")

    def log_file(self, event):
        # don't log changes to own log or a recursive loop will trigger
        if abspath(event.src_path) == abspath(self.log_path):
            return

        event_time_tuple = (event.event_type, datetime.now().timestamp())
        # TODO: this will bloat up quickly, delete somehow something somewhere
        #  (if list is longer than x and  delete is last entry then delete older than a day)
        try:
            self.file_log[abspath(event.src_path)].append(event_time_tuple)
        except KeyError:
            self.file_log[abspath(event.src_path)] = [event_time_tuple]

        with open(self.log_path, "w") as fp:  # TODO heavy usage of open and close probably better to only open once ?
            json.dump(self.file_log, fp, indent=2)

    def on_created(self, event: Union[FileCreatedEvent, DirCreatedEvent]):
        self.log_file(event)

        print(f"hey, {event.src_path} has been created! {event.event_type}")

    def on_deleted(self, event: Union[FileDeletedEvent, DirDeletedEvent]):
        self.log_file(event)

        print(f"what the f**k! Someone deleted {event.src_path}! {event.event_type}")

    def on_modified(self, event: Union[FileModifiedEvent, DirModifiedEvent]):
        self.log_file(event)

        print(f"hey buddy, {event.src_path} has been modified {event.event_type}")

    # FIXME: Windows 10: renaming a file = on_moved for the old name and modified for new file(no create),
    #  moving a file = delete, create, modify
    def on_moved(self, event: Union[FileMovedEvent, DirMovedEvent]):
        self.log_file(event)

        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path} {event.event_type}")

    def start_handler(self):
        if os.path.isfile(self.log_path):
            with open(self.log_path, "r") as fp:
                self.file_log = json.load(fp)

        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = True  # for backup we don't need directories right? Filepath should all we need
        case_sensitive = False  # TODO change for linux
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_deleted = self.on_deleted
        my_event_handler.on_modified = self.on_modified
        my_event_handler.on_moved = self.on_moved

        go_recursively = True
        my_observer = Observer()
        for path in self.config["paths"]:
            my_observer.schedule(my_event_handler, path, recursive=go_recursively)

        my_observer.start()
