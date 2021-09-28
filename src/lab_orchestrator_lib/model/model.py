"""Contains the dataclasses that are used in this project."""
from typing import Union, List

from lab_orchestrator_lib.custom_exceptions import ValidationError


Identifier = Union[str, int]


class Model:
    """Abstract base class that is used for all classes that should be saved in a database."""

    def __init__(self, primary_key: Identifier):
        """Initializes a model object.

        :param primary_key: A unique value to identify the object. (if string, min. 1 char)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        if isinstance(primary_key, str) and len(primary_key) <= 0:
            raise ValidationError("primary key is too short.")
        self.primary_key = primary_key


def check_dns_name(name) -> bool:
    """Checks if the name is a valid dns label.
    
    Definition: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names

    :param name: The name to check.
    :return: If the dns name is valid.
    """
    alphabetic = "abcdefghijklmnopqrstuvwxyz"
    alphanumeric = alphabetic + "1234567890"
    allowed_chars = alphanumeric + "-"
    if len(name) <= 0:
        return False
    if len(name) > 63:
        return False
    # contain only lowercase alphanumeric characters or '-'
    for char in name:
        if char not in allowed_chars:
            return False
    # start with an alphabetic character
    if name[0] not in alphabetic:
        return False
    # end with an alphanumeric character
    if name[len(name) - 1] not in alphanumeric:
        return False
    return True


def check_dns_subdomain_name(name) -> bool:
    """Checks if the name is a valid dns subdomain name.

    Definition: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names

    :param name: The name to check.
    :return: If the dns subdomain name is valid.
    """
    alphabetic = "abcdefghijklmnopqrstuvwxyz"
    alphanumeric = alphabetic + "1234567890"
    allowed_chars = alphanumeric + "-."
    if len(name) <= 0:
        return False
    if len(name) > 253:
        return False
    # contain only lowercase alphanumeric characters or '-' or '.'
    for char in name:
        if char not in allowed_chars:
            return False
    # start with an alphanumeric character
    if name[0] not in alphanumeric:
        return False
    # end with an alphanumeric character
    if name[len(name) - 1] not in alphanumeric:
        return False
    return True


class User(Model):
    """A User of the library."""

    def __init__(self, primary_key: Identifier):
        """Initializes a user object.

        :param primary_key: A unique value to identify the object. (if string, max. 12 chars and needs to be a valid dns label)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        if isinstance(primary_key, str):
            if len(primary_key) > 12:
                raise ValidationError("primary key is longer than 12 characters.")
            if not check_dns_name(primary_key):
                raise ValidationError("primary key contains illegal characters.")
        super().__init__(primary_key)


class DockerImage(Model):
    """Link to a Docker Image that contains a VM image.

    A docker image object is a link to a docker image that contains a VM image. This is used to create labs. If your
    image is in docker hub the link only needs to contain `username/reponame:version` and no `https://...` stuff.
    """
    def __init__(self, primary_key: Identifier, name: str, description: str, url: str):
        """Initializes a docker image object.

        :param primary_key: A unique value to identify the object.
        :param name: The name of the docker image. (min. 1 char, max. 32 chars)
        :param description: A short description of the docker image. (min. 1 char, max. 128 chars)
        :param url: The url to the image. (min. 1 char, max. 256 chars)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        super().__init__(primary_key)
        if len(name) <= 0:
            raise ValidationError("name is too short.")
        if len(name) > 32:
            raise ValidationError("name is longer than 32 characters.")
        if len(description) <= 0:
            raise ValidationError("description is too short.")
        if len(description) > 128:
            raise ValidationError("description is longer than 128 characters.")
        # TODO: more validation for url
        if len(url) <= 0:
            raise ValidationError("url is too short.")
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
        :param docker_image_name: Name of the VM. (valid dns subdomain)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        super().__init__(primary_key)
        self.lab_id = lab_id
        self.docker_image_id = docker_image_id
        if not check_dns_subdomain_name(docker_image_name):
            raise ValidationError("docker_image_name is not a valid dns subdomain")
        self.docker_image_name = docker_image_name


class Lab(Model):
    """Lab is a combination of VMs that can be started.

    When you start a lab a lab_instance will be created and the VMs are started in Kubernetes. A lab is used
    to combine VMs in a scenario.
    """

    def __init__(self, primary_key: Identifier, name: str, namespace_prefix: str, description: str):
        """Initializes a lab object.

        :param primary_key: A unique value to identify the object.
        :param name: The name of the lab. (min. 1 char, max. 32 chars)
        :param namespace_prefix: A prefix that is used in the namespace in Kubernetes where the VMs are started. (max. 32 chars and needs to be a valid dns label)
        :param description: A short description of the docker image. (min. 1 char, max. 128 chars)
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        super().__init__(primary_key)
        if len(name) <= 0:
            raise ValidationError("name is too short.")
        if len(name) > 32:
            raise ValidationError("name is longer than 32 characters.")
        if len(namespace_prefix) > 32:
            raise ValidationError("namespace_prefix is longer than 32 characters.")
        if not check_dns_name(namespace_prefix):
            raise ValidationError("namespace_prefix is not a valid dns label.")
        if len(description) <= 0:
            raise ValidationError("description is too short.")
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

        :param primary_key: A unique value to identify the object. (if string, max. 16 chars and needs to be a valid dns label)
        :param lab_id: The id of the lab that is started.
        :param user_id: The id of the user that has started the lab.
        :raise ValidationError: if one of the parameters has an invalid value.
        """
        if isinstance(primary_key, str):
            if len(primary_key) > 16:
                raise ValidationError("primary key is longer than 16 characters.")
            if not check_dns_name(primary_key):
                raise ValidationError("primary key is not a valid dns label")
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

        :param primary_key: A unique value to identify the object. (if string, max. 14 chars)
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
