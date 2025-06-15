import json

data = json.load(open("testdata/test_data.json", encoding="utf-8"))

class DataProvider:

    def __init__(self) -> None:
        self.config = data

    def get(self, prop) -> str:
        return self.config.get(prop)