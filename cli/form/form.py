from typing import List
from . import form_item


class Form:
    def __init__(self, items: List[form_item.FormItem]):
        self.items = items
