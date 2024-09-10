# Config class to hold the mandatory Mantis variables
class MantisConfig:
    def __init__(self, config):
        self.base_url = config['base_url']
        self.api_token = config['api_token']
        self.project_id = config['project_id']
        self.time_zone = config['time_zone']
        self.issue_fields = [field.strip() for field in config['issue_fields'].split(',')]
        self.work_notes_fields = [field.strip() for field in config['work_notes_fields'].split(',')]
        self.page_size = config['page_size']
