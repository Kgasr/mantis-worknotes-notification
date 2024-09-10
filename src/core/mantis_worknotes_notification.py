import json
import base64
from src.utils.logger import CustomLogger
from src.utils.read_file import read_yaml
from src.handlers.msmq_handler import MsmqHandler
from src.handlers.mantis_handler import MantisHandler


class MantisWorkNotesNotification:
    def __init__(self, config_file, time_window=5, custom_logger=None, ):
        self.__time_window = time_window
        self.__msmq_client = None
        self.__config_file = config_file
        self.__config = read_yaml(self.__config_file)
        if custom_logger is None:
            self.__custom_logger = CustomLogger(self.__config_file).get_logger()
        else:
            self.__custom_logger = custom_logger

    # Main method of class to start the process.
    def mantis_worknotes_notification(self):
        try:
            self.__custom_logger.info("Mantis work-notes notification process started")
            issues, notes = self.__get_data_from_mantis_api()
            if issues or notes:
                msg = self.__send_data_to_queue(issues, notes)
            else:
                msg = "No Data available to be sent to queue"
                self.__custom_logger.info(msg)
            self.__custom_logger.info("Mantis work-notes notification process ended")
            return msg
        except Exception as e:
            msg = f"Mantis work-notes notification process failed : {e}"
            self.__custom_logger.error(msg)
            raise Exception(msg)

    # Method to load mantis config and
    # invoke Mantis API call using Mantis handler to fetch updated issues in given time window
    def __get_data_from_mantis_api(self):
        try:
            self.__custom_logger.info("Fetching data from Mantis started")
            mantis_client = MantisHandler(self.__config)
            issues, notes = mantis_client.fetch_recently_updated_issues(self.__time_window)
            self.__custom_logger.info("Fetching data from Mantis completed")
            return issues, notes
        except Exception as e:
            msg = f"Error fetching data from Mantis API: {e}"
            self.__custom_logger.error(msg)
            raise Exception(msg)

    # Method to load MSMQ config and send data to MSMQ using MSMQ handler
    def __send_data_to_queue(self, issues, notes):
        try:
            self.__custom_logger.info("Sending data to MSMQ started")
            self.__msmq_client = MsmqHandler(self.__config['msmq'])
            if issues:
                self.__send_issues_to_queue(issues)
            if notes:
                self.__send_notes_to_queue(notes)
            msg = "Data Successfully sent to queue"
            self.__custom_logger.info(f"Sending data to MSMQ ended - {msg}")
            return msg
        except Exception as e:
            msg = f"Error sending data to MSMQ: {e}"
            self.__custom_logger.error(msg)
            raise Exception(msg)

    # Method to prepare label for new issue and send to queue
    def __send_issues_to_queue(self, issues_data):
        for issue in issues_data:
            label = self.__config['issue_label_formatter'].format(**issue)
            self.__send_to_queue(label,issue)
            self.__custom_logger.info(f"Sent issue to queue: {label}")

    # Method to prepare label for new work note and send to queue
    def __send_notes_to_queue(self, notes_data):
        for note in notes_data:
            label = self.__config['note_label_formatter'].format(**note)
            self.__send_to_queue(label,note)
            self.__custom_logger.info(f"Sent work note to queue: {label}")

    # Method to send data to queue
    def __send_to_queue(self, label, data_to_send):
        body = json.dumps(data_to_send, indent=4)
        encoded_body = base64.b64encode(body.encode('utf-8')).decode('utf-8')
        self.__msmq_client.send_message(label, encoded_body)