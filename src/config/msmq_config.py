# Config class to hold the mandatory MSMQ variables
class MsmqConfig:
    def __init__(self, config):
        self.queue = config['queue']
