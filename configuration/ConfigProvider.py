import configparser

config = configparser.ConfigParser()
config.read("configuration/test_config.ini")

class ConfigProvider:

    def __init__(self) -> None:
        self.config = config

    def get(self, section, prop) -> str:
        return self.config[section].get(prop)

    def get_int(self, section, prop) -> int:
        return self.config[section].getint(prop)