class FormItem:
    def __init__(self, key, message, validator=None):
        self.key = key
        self.message = message
        self.validator = validator
        self.value = None

    def set_value(self, value):
        self.value = value
