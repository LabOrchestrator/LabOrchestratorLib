from typing import Generic, List, TypeVar, Any

from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance

Adapter = TypeVar('Adapter')
LibModelType = TypeVar('LibModelType', DockerImage, Lab, LabInstance)  # subclasses of Model


class AdapterController(Generic[Adapter, LibModelType]):
    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    def get_all(self) -> List[LibModelType]:
        return self.adapter.get_all()

    def get(self, identifier) -> LibModelType:
        return self.adapter.get(identifier)

    def get_by_attr(self, attr, value) -> LibModelType:
        return self.adapter.get_by_attr(attr, value)

    def delete(self, identifier) -> None:
        return self.adapter.delete(identifier)

    def save(self, obj: LibModelType) -> LibModelType:
        return self.adapter.save(obj)

    def filter(self, **kwargs) -> LibModelType:
        return self.adapter.filter(**kwargs)