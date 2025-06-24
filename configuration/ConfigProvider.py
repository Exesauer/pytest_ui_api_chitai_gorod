import configparser

config = configparser.ConfigParser()
config.read("./configuration/test_config.ini")


class ConfigProvider:
    """Класс для управления конфигурациями из файла test_config.ini."""

    def __init__(self) -> None:
        """Инициализация класса, загрузка конфигураций из файла."""
        self.config = config

    def get(self, section, prop) -> str:
        """Получение значения свойства из указанного раздела как строку.

        :param section: str: Название раздела конфигурационного файла.
        :param prop: str: Название свойства, значение которого нужно получить.

        :returns: str: Значение свойства.
        """
        return self.config[section].get(prop)

    def get_int(self, section, prop) -> int:
        """Получение значения свойства из указанного раздела как целое число.

        :param section: str: Название раздела конфигурационного файла.
        :param prop: str: Название свойства, значение которого нужно получить.

        :returns: str: Значение свойства.
        """
        return self.config[section].getint(prop)
