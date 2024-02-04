from . import form as form_model


class FormGenerator:
    def __init__(self, form: form_model.Form):
        self.form = form

    def generate(self) -> dict:
        items = self.form.items

        result = {}

        for item in items:
            result[item.key] = input(item.message)

        return result
