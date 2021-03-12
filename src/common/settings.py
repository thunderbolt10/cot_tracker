import logging
import json

class Settings():
    """
    This class loads the settings.cfg json file into a local dictionary
    """
    def __init__(self):
        self.config = {}
        self.log = logging.getLogger(__name__)

    def load(self, settings_file):
        self.log.info('load settings from: %s', settings_file)
        with open(settings_file) as fp:
            self.config = json.load(fp)

        self.log.info(self.config)