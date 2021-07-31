import time
from watchdog.observers import Observer
from watchdog.events import *  # PatternMatchingEventHandler
import json
from os.path import abspath

class WatchdogHandler:
    def __init__(self, config: dict):
        self.config = config
        self.file_log = {}

    def log_file(self, event):
        # TODO: this will bloat up quickly delete somehow something somewhere
        try:
            self.file_log[abspath(event.src_path)].append(event.event_type)
        except KeyError:
            self.file_log[abspath(event.src_path)] = [event.event_type]

        with open("test.log", "w") as fp:
            json.dump(self.file_log, fp, indent=2)

    def on_created(self, event: FileCreatedEvent):
        self.log_file(event)

        print(f"hey, {event.src_path} has been created! {event.event_type}")

    def on_deleted(self, event: FileDeletedEvent):
        self.log_file(event)

        print(f"what the f**k! Someone deleted {event.src_path}! {event.event_type}")

    def on_modified(self, event: FileModifiedEvent):
        self.log_file(event)

        print(f"hey buddy, {event.src_path} has been modified {event.event_type}")

    def on_moved(self, event: FileMovedEvent):  # FIXME: on my windows 10 it deletes, creates, and modifies "on move"
        self.log_file(event)

        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path} {event.event_type}")


    def start_handler(self):
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
        try:  # TODO remove?
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()
