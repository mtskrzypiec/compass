from driver import driver


class Project:
    def __init__(self, name: str, product: str, driver: driver.Driver, initial_steps, running_steps):
        self.name = name
        self.product = product
        self.driver = driver
        self.initial_steps = initial_steps
        self.running_steps = running_steps
