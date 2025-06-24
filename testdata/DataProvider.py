import json

data = json.load(open("./testdata/test_data.json", encoding="utf-8"))


class DataProvider:
    """Класс предназначен для работы с конфигурационными данными, загружаемыми из файла test_data.json."""

    def __init__(self) -> None:
        """Инициализация класса и загрузка конфигурационных данных в атрибут config."""
        self.config = data

    def get(self, prop) -> str:
        """Получение значения свойства из конфигурационных данных.

        :param prop: имя свойства, значение которого нужно получить.

        :return: Значение конкретного свойства или None, если свойство не найдено.
        """
        return self.config.get(prop)
