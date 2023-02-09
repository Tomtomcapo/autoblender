import yaml
from yaml.loader import SafeLoader

from singleton import Singleton


class SettingsParser(object):
    __metaclass__ = Singleton

    @staticmethod
    def parse(settings_file: str):
        """
        Parse settings file.
        :param settings_file:
        :return:
        """
        with open(settings_file) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data
