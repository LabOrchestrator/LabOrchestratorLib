"""Contains all adapters that needs to be implemented to use the lab orchestrator lib."""
from typing import List, Any, Dict

from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance, Identifier, User, LabDockerImage


class UserAdapterInterface:
    """Adapter that is used to connect the user model to the database.

    Contains only get methods, because the lab_controller_lib won't create or delete users.
    """

    def get_all(self) -> List[User]:
        """Gives a list of all users.

        :return: A list of all users.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> User:
        """Gives a specific user.

        :param identifier: The identifier of the user.
        :return: A specific user.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()


class DockerImageAdapterInterface:
    """Adapter that is used to connect the docker image model to the database."""

    def create(self, name: str, description: str, url: str) -> DockerImage:
        """Creates a docker image and saves it to the database.

        :param name: Name of the docker image.
        :param description: Description of the docker image.
        :param url: Url of the docker image.
        :return: A newly added docker image.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get_all(self) -> List[DockerImage]:
        """Gives all docker images.

        :return: A list of all docker images.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> DockerImage:
        """Gives a specific docker image.

        :param identifier: The identifier of the docker image.
        :return: The specific docker image.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        """Deletes a specific docker image.

        :param identifier: The identifier of the docker image.
        :return: None
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def save(self, obj: DockerImage) -> DockerImage:
        """Saves changes of the docker image to the database.

        :param obj: The docker image object that contains changes.
        :return: The docker image.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> List[DockerImage]:
        """Filters the docker images and returns all docker images that matches the filter criteria.

        The database should be filtered by the attributes and belonging values that are given in the kwargs dictionary.

        :param kwargs: A dictionary with filters.
        :return: All docker images that matches the filters.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()


class LabDockerImageAdapterInterface:
    """Adapter that is used to connect the lab docker image model to the database."""

    def create(self, lab_id: Identifier, docker_image_id: Identifier, docker_image_name: str) -> LabDockerImage:
        """Creates a lab docker image and saves it to the database.

        :param lab_id: Id of the lab.
        :param docker_image_id: Id of the docker image.
        :param docker_image_name: Name of the VM.
        :return: A newly added lab docker image.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get_all(self) -> List[LabDockerImage]:
        """Gives all lab docker images.

        :return: A list of all lab docker images.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> LabDockerImage:
        """Gives a specific lab docker image.

        :param identifier: The identifier of the lab docker image.
        :return: The specific lab docker image.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        """Deletes a specific lab docker image.

        :param identifier: The identifier of the lab docker image.
        :return: None
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def save(self, obj: LabDockerImage) -> LabDockerImage:
        """Saves changes of the lab docker image to the database.

        :param obj: The lab docker image object that contains changes.
        :return: The lab docker image.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> List[LabDockerImage]:
        """Filters the lab docker images and returns all lab docker images that matches the filter criteria.

        The database should be filtered by the attributes and belonging values that are given in the kwargs dictionary.

        :param kwargs: A dictionary with filters.
        :return: All lab docker images that matches the filters.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()


class LabAdapterInterface:
    """Adapter that is used to connect the lab model to the database."""

    def create(self, name: str, namespace_prefix: str, description: str) -> Lab:
        """Creates a lab and saves it to the database.

        :param name: Name of the lab.
        :param namespace_prefix: Namespace prefix of the lab.
        :param description: Description of the lab.
        :return: A newly added lab.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get_all(self) -> List[Lab]:
        """Gives all labs.

        :return: A list of all labs.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> Lab:
        """Gives a specific lab.

        :param identifier: The identifier of the lab.
        :return: The specific lab.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        """Deletes a specific lab.

        :param identifier: The identifier of the lab.
        :return: None
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def save(self, obj: Lab) -> Lab:
        """Saves changes of the lab to the database.

        :param obj: The lab object that contains changes.
        :return: The lab.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> List[Lab]:
        """Filters the labs and returns all labs that matches the filter criteria.

        The database should be filtered by the attributes and belonging values that are given in the kwargs dictionary.

        :param kwargs: A dictionary with filters.
        :return: All labs that matches the filters.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()


class LabInstanceAdapterInterface:
    """Adapter that is used to connect the lab instance model to the database."""

    def create(self, lab_id: Identifier, user_id: Identifier) -> LabInstance:
        """Creates a lab instance and saves it to the database.

        :param lab_id: Lab id of the lab instance.
        :param user_id: User id of the lab instance.
        :return: A newly added lab instance.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get_all(self) -> List[LabInstance]:
        """Gives all lab instances.

        :return: A list of all lab instances.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get(self, identifier: Identifier) -> LabInstance:
        """Gives a specific lab instance.

        :param identifier: The identifier of the lab instance.
        :return: The specific lab instance.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def delete(self, identifier: Identifier) -> None:
        """Deletes a specific lab instance.

        :param identifier: The identifier of the lab instance.
        :return: None
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def save(self, obj: LabInstance) -> LabInstance:
        """Saves changes of the lab instance to the database.

        :param obj: The lab instance object that contains changes.
        :return: The lab instance.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def filter(self, **kwargs: Dict[str, Any]) -> List[LabInstance]:
        """Filters the lab instances and returns all lab instances that matches the filter criteria.

        The database should be filtered by the attributes and belonging values that are given in the kwargs dictionary.

        :param kwargs: A dictionary with filters.
        :return: All lab instances that matches the filters.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()
