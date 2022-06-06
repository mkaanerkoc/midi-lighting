class Command(object):
    def __init__(self, call, **kwargs):
        self._command = call
        self._kwargs = kwargs

    def execute(self):
        if self._command:
            self._command(**self._kwargs)

