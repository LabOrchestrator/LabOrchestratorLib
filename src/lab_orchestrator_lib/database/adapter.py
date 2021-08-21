from typing import List, Any, Dict

from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance, Identifier, User


class UserAdapterInterface:
    """

    Contains only get methods, because the lab_controller_lib won't create or delete users.
    """
    def get_all(self) -> List[User]:
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> User:
        raise NotImplementedError()


class DockerImageAdapterInterface:
    def create(self, name: str, description: str, url: str) -> DockerImage:
        raise NotImplementedError()

    def get_all(self) -> List[DockerImage]:
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> DockerImage:
        raise NotImplementedError()

    def get_by_attr(self, attr: str, value: Any) -> DockerImage:
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        raise NotImplementedError()

    def save(self, obj: DockerImage) -> DockerImage:
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> DockerImage:
        raise NotImplementedError()


class LabAdapterInterface:
    def create(self, name: str, namespace_prefix: str, description: str, docker_image_id: Identifier,
               docker_image_name: str) -> Lab:
        raise NotImplementedError()

    def get_all(self) -> List[Lab]:
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> Lab:
        raise NotImplementedError()

    def get_by_attr(self, attr: str, value: Any) -> Lab:
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        raise NotImplementedError()

    def save(self, obj: Lab) -> Lab:
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> Lab:
        raise NotImplementedError()


class LabInstanceAdapterInterface:
    def create(self, lab_id: Identifier, user_id: Identifier) -> LabInstance:
        raise NotImplementedError()

    def get_all(self) -> List[LabInstance]:
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> LabInstance:
        raise NotImplementedError()

    def get_by_attr(self, attr: str, value: Any) -> LabInstance:
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        raise NotImplementedError()

    def save(self, obj: LabInstance) -> LabInstance:
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> LabInstance:
        raise NotImplementedError()
