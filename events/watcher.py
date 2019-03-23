from threading import Thread
from time import sleep
from event import Event


class Watcher:

    thread = None
    to_watch = None

    def __init__(self, state_func, change_handlers, initial_state=None, state_check_interval=None, *state_func_args, **state_func_kwargs):
        self.state_func = state_func
        self.initial_state = initial_state
        self.state_check_interval = state_check_interval
        self.change_handlers = change_handlers
        self.state_func_args = state_func_args
        self.state_func_kwargs = state_func_kwargs
        self.event = Event()
        for handler in self.change_handlers:
            self.event.add_handler(handler)

    def start_watching(self):
        if not self.thread:
            self.to_watch = True
            self.thread = Thread(target=self.process_watcher, daemon=True)
            self.thread.start()
            self.thread.join()

    def process_watcher(self):
        previous_state = self.initial_state
        while self.to_watch:
            current_state = self.state_func(
                *self.state_func_args, **self.state_func_kwargs)
            if current_state != previous_state:
                self.event.fire(previous_state, current_state)
                previous_state = current_state
            if self.state_check_interval:
                sleep(self.state_check_interval)

    def stop_watching(self):
        self.to_watch = False
