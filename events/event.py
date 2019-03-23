class Event:
    def __init__(self):
        self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)

    def remove_handler(self, handler):
        self.handlers.discard(handler)

    def fire(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

    def get_handler_count(self):
        return len(self.handlers)

    __iadd__ = add_handler
    __isub__ = remove_handler
    __call__ = fire
    __len__ = get_handler_count
