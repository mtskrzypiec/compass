
class Project:
    def __init__(self, name: str, product: str):
        self.name = name
        self.product = product

    def getName(self) -> str:
        return self.name
