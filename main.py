import logging
from src import MantisWorkNotesNotification, CustomLogger

config_file = 'config.yaml'


# Main method to trigger the process.
# Time_window is the time in minutes window for issues/notes extraction
def main():
    try:
        custom_logger = CustomLogger(config_file).get_logger()
        custom_logger.info(f"Process Initiated")
        mantis_notification = MantisWorkNotesNotification(config_file=config_file,
                                                          time_window=5,
                                                          custom_logger=custom_logger)
        result = mantis_notification.mantis_worknotes_notification()
        custom_logger.info(f"Process ended with result : '{result}'")
    except Exception as ex:
        # Set up a default logger if there's an issue
        logging.basicConfig(filename='error.log',
                            level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"An error occurred during execution: '{ex}'")


if __name__ == '__main__':
    main()
