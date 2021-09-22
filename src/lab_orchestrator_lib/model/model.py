"""Contains the dataclasses that are used in this project."""
from typing import Union, List

from lab_orchestrator_lib.custom_exceptions import ValidationError


Identifier = Union[str, int]


class Model:
    """Abstract base class that is used for all classes that should be saved in a database."""

    def __init__(self, primary_key: Identifier):
        """Initializes a model object.

        :param primary_key: A unique value to identify the object.
        """
        self.primary_key = primary_key


class User(Model):
    """A User of the library."""

    def __init__(self, primary_key: Identifier):
        """Initializes a user object.

        :param primary_key: A unique value to identify the user.
        """
        super().__init__(primary_key)


class DockerImage(Model):
    """Link to a Docker Image that contains a VM image.

    A docker image object is a link to a docker image that contains a VM image. This is used to create labs. If your
    image is in docker hub the link only needs to contain `username/reponame:version` and no `https://...` stuff.
    """
    def __init__(self, primary_key: Identifier, name: str, description: str, url: str):
        """Initializes a docker image object.

        :param primary_key: A unique value to identify the object.
        :param name: The name of the docker image. (max. 32 chars)
        :param description: A short description of the docker image. (max. 128 chars)
        :param url: The url to the image. (max. 256 chars)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        super().__init__(primary_key)
        if len(name) > 32:
            raise ValidationError("name is longer than 32 characters.")
        if len(description) > 128:
            raise ValidationError("description is longer than 128 characters.")
        if len(url) > 256:
            raise ValidationError("url is longer than 256 characters.")
        self.name = name
        self.description = description
        self.url = url


class LabDockerImage(Model):
    """A Lab Docker Image is a docker image that is referenced to a lab.

    This is needed to have multiple VMs in one lab.
    """

    def __init__(self, primary_key: Identifier, lab_id: Identifier, docker_image_id: Identifier,
                 docker_image_name: str):
        """Initializes a lab docker image.

        :param primary_key: A unique value to identify the object.
        :param lab_id: Id of the lab.
        :param docker_image_id: Id of the docker image.
        :param docker_image_name: Name of the VM.
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        super().__init__(primary_key)
        self.lab_id = lab_id
        self.docker_image_id = docker_image_id
        if len(docker_image_name) > 32:
            raise ValidationError("docker_image_name is longer than 32 characters.")
        self.docker_image_name = docker_image_name


class Lab(Model):
    """Lab is a combination of VMs that can be started.

    When you start a lab a lab_instance will be created and the VMs are started in Kubernetes. A lab is used
    to combine VMs in a scenario.
    """

    def __init__(self, primary_key: Identifier, name: str, namespace_prefix: str, description: str):
        """Initializes a lab object.

        :param primary_key: A unique value to identify the object.
        :param name: The name of the lab. (max. 32 chars)
        :param namespace_prefix: A prefix that is used in the namespace in Kubernetes where the VMs are started. (max. 32 chars)
        :param description: A short description of the docker image. (max. 128 chars)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        super().__init__(primary_key)
        if len(name) > 32:
            raise ValidationError("name is longer than 32 characters.")
        if len(namespace_prefix) > 32:
            raise ValidationError("namespace_prefix is longer than 32 characters.")
        if len(description) > 128:
            raise ValidationError("description is longer than 128 characters.")
        self.name = name
        self.namespace_prefix = namespace_prefix
        self.description = description


class LabInstance(Model):
    """A lab instance is a lab that is started by a user.

    A lab instance is linked to many Kubernetes resources. Lab instances are created by the controllers when you start
    a lab. When you create them by your own you're probably doing something wrong.
    """

    def __init__(self, primary_key: Identifier, lab_id: Identifier, user_id: Identifier):
        """Initializes a lab instance object.

        :param primary_key: A unique value to identify the object.
        :param lab_id: The id of the lab that is started.
        :param user_id: The id of the user that has started the lab.
        """
        super().__init__(primary_key)
        self.lab_id = lab_id
        self.user_id = user_id


class LabInstanceKubernetes(Model):
    """A lab instance with a token.

    Doesn't need any adapter and should not be saved in the database. This is used to return the JWT access token when
    the lab is started.
    """
    def __init__(self, primary_key: Identifier, lab_id: Identifier, user_id: Identifier, jwt_token: str,
                 allowed_vmis: List[str]):
        """Initializes a lab instance kubernetes object.

        :param primary_key: A unique value to identify the object.
        :param lab_id: The id of the lab that is started.
        :param user_id: The id of the user that has started the lab.
        :param jwt_token: JWT token that can be used to access the VMs in this lab instance.
        :param allowed_vmis: List of VMI names that the user is allowed to open.
        """
        super().__init__(primary_key)
        self.lab_id = lab_id
        self.user_id = user_id
        self.jwt_token = jwt_token
        self.allowed_vmis = allowed_vmis
