class CallRecord:
    def __init__(self, caller, called, timestamp, duration):
        self.caller = caller
        self.called = called
        self.timestamp = timestamp
        self.duration = duration # Seconds
