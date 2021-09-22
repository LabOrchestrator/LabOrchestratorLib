"""Contains a generic controller that can be used for adapters."""
from typing import Generic, List, TypeVar, Any

from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance

Adapter = TypeVar('Adapter')
LibModelType = TypeVar('LibModelType', DockerImage, Lab, LabInstance)  # subclasses of Model


class AdapterController(Generic[Adapter, LibModelType]):
    """Generic controller for adapter classes.

    This generic class implements some of the methods that are needed for a adapter controller. Whats missing is the
    create method and some specific methods that can't be abstracted.
    """

    def __init__(self, adapter: Adapter):
        """Initializes an adapter controller.

        :param adapter: The adapter of the controller.
        """
        self.adapter = adapter

    def get_all(self) -> List[LibModelType]:
        """Gives all objects of the adapter.

        :return: A list of all objects of the adapter.
        """
        return self.adapter.get_all()

    def get(self, identifier) -> LibModelType:
        """Gives a specific object of the adapter.

        :param identifier: The identifier of the object.
        :return: The specific object.
        """
        return self.adapter.get(identifier)

    def delete(self, identifier) -> None:
        """Deletes a specific object of the adapter.

        :param identifier: The identifier of the object.
        :return: None
        """
        return self.adapter.delete(identifier)

    def save(self, obj: LibModelType) -> LibModelType:
        """Saves changes of the object to the database.

        :param obj: The object object that contains changes.
        :return: The object.
        """
        return self.adapter.save(obj)

    def filter(self, **kwargs) -> List[LibModelType]:
        """Filters the objects of the adapter and returns all objects that matches the filter criteria.

        The database should be filtered by the attributes and belonging values that are given in the kwargs dictionary.

        :param kwargs: A dictionary with filters.
        :return: All objects that matches the filters.
        """
        return self.adapter.filter(**kwargs)
