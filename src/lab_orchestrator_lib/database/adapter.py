from typing import List

from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance


class DockerImageAdapter:
    def create(self, obj: DockerImage) -> DockerImage:
        raise NotImplementedError()

    def get_all(self) -> List[DockerImage]:
        raise NotImplementedError()

    def get(self, identifier) -> DockerImage:
        raise NotImplementedError()

    def get_by_attr(self, attr, value) -> DockerImage:
        raise NotImplementedError()

    def delete(self, identifier) -> None:
        raise NotImplementedError()

    def save(self, obj: DockerImage) -> DockerImage:
        raise NotImplementedError()

    def filter(self, **kwargs) -> DockerImage:
        raise NotImplementedError()


class LabAdapter:
    def create(self, obj: Lab) -> Lab:
        raise NotImplementedError()

    def get_all(self) -> List[Lab]:
        raise NotImplementedError()

    def get(self, identifier) -> Lab:
        raise NotImplementedError()

    def get_by_attr(self, attr, value) -> Lab:
        raise NotImplementedError()

    def delete(self, identifier) -> None:
        raise NotImplementedError()

    def save(self, obj: Lab) -> Lab:
        raise NotImplementedError()

    def filter(self, **kwargs) -> Lab:
        raise NotImplementedError()


class LabInstanceAdapter:
    def create(self, obj: LabInstance) -> LabInstance:
        raise NotImplementedError()

    def get_all(self) -> List[LabInstance]:
        raise NotImplementedError()

    def get(self, identifier) -> LabInstance:
        raise NotImplementedError()

    def get_by_attr(self, attr, value) -> LabInstance:
        raise NotImplementedError()

    def delete(self, identifier) -> None:
        raise NotImplementedError()

    def save(self, obj: LabInstance) -> LabInstance:
        raise NotImplementedError()

    def filter(self, **kwargs) -> LabInstance:
        raise NotImplementedError()
