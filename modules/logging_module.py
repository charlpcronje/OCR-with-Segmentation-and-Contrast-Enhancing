# modules/logging_module.py

import logging
import os
from datetime import datetime

class LoggingModule:
    def __init__(self, config):
        self.logger = logging.getLogger('OCRApp')
        self.logger.setLevel(getattr(logging, config.get('logging')['level'], logging.INFO))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console Handler
        if config.get('logging')['console']:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        # File Handler
        if config.get('logging')['file']:
            logs_folder = os.path.join(config.env_config['LOGS_FOLDER_PATH'])
            os.makedirs(logs_folder, exist_ok=True)
            log_filename = os.path.join(logs_folder, f"logs-{datetime.now().date()}.log")
            fh = logging.FileHandler(log_filename)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
