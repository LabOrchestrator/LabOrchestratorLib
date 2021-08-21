from typing import Union

from lab_orchestrator_lib.custom_exceptions import ValidationError


Identifier = Union[str, int]


class Model:
    def __init__(self, primary_key: Identifier):
        self.primary_key = primary_key


class User(Model):
    def __init__(self, primary_key: Identifier):
        super().__init__(primary_key)


class DockerImage(Model):
    def __init__(self, primary_key: Identifier, name: str, description: str, url: str):
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


class Lab(Model):
    def __init__(self, primary_key: Identifier, name: str, namespace_prefix: str, description: str,
                 docker_image_id: Identifier, docker_image_name: str):
        super().__init__(primary_key)
        if len(name) > 32:
            raise ValidationError("name is longer than 32 characters.")
        if len(namespace_prefix) > 32:
            raise ValidationError("namespace_prefix is longer than 32 characters.")
        if len(description) > 128:
            raise ValidationError("description is longer than 128 characters.")
        if len(docker_image_name) > 32:
            raise ValidationError("docker_image_name is longer than 32 characters.")
        self.name = name
        self.namespace_prefix = namespace_prefix
        self.description = description
        self.docker_image_id = docker_image_id
        self.docker_image_name = docker_image_name


class LabInstance(Model):
    def __init__(self, primary_key: Identifier, lab_id: Identifier, user_id: Identifier):
        super().__init__(primary_key)
        self.lab_id = lab_id
        self.user_id = user_id


class LabInstanceKubernetes(Model):
    """Doesn't need any adapter and should not be saved in the database. This is used to return information about a
    lab instance including information from kubernetes and the jwt token."""
    def __init__(self, primary_key: Identifier, lab_id: Identifier, user_id: Identifier, jwt_token: str):
        super().__init__(primary_key)
        self.lab_id = lab_id
        self.user_id = user_id
        self.jwt_token = jwt_token


