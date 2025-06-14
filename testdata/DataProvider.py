import json

data = json.load(open("./test_data.json"))

class DataProvider:

    def __init__(self) -> None:
        self.config = data

    def get(self, prop) -> str:
        return self.config.get(prop)