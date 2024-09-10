# Config class to hold the mandatory MySQL variables
class MysqlConfig:
    def __init__(self, config):
        self.host = config['host']
        self.user = config['user']
        self.password = config['password']
        self.database = config['database']
        self.charset = config['charset']
