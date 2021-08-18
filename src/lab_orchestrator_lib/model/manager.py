from dataclasses import dataclass
from typing import List, Optional, Any, Union, Dict

from lab_orchestrator_lib.model.model import Identifier, Model

Items = Dict[Identifier, Any]
Item = Model


class Manager:
    def __init__(self, items: Optional[Items] = None):
        if items is None:
            items = {}
        self.items: Items = items

    def get(self, primary_key: Identifier) -> Optional[Item]:
        return self.items.get(primary_key, None)

    def delete(self, item: Item) -> None:
        """Deletes the item.
        :param item: The item that should be deleted
        :return: None
        :raise: KeyError
        """
        del self.items[item.primary_key]

    def add(self, item: Item):
        self.items[item.primary_key] = item
