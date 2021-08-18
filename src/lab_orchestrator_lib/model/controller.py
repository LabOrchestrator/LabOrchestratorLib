from abc import ABC
from typing import Type

from lab_orchestrator_lib.model.manager import Manager
from lab_orchestrator_lib.model.model import Model

Item = Model


class ModelController(ABC):
    def __init__(self, manager: Manager, model: Type[Item]):
        self.manager = manager
        self.model = model

    def get_list(self):
        return [item for item in self.manager.items.values()]

    def _create(self, *args, **kwargs) -> Item:
        return self.model(*args, **kwargs)

    def get(self, id) -> Item:
        obj = self.manager.get(id)
        if obj is None:
            raise KeyError(f"Key error: {id}")
        return obj

    def delete(self, obj: db.Model):
        db.session.delete(obj)
        db.session.commit()

    def _serialize(self, obj):
        raise NotImplementedError()

    def make_response(self, inp: Union[db.Model, List[db.Model]]):
        if isinstance(inp, list):
            return jsonify([self._serialize(obj) for obj in inp])
        return jsonify(self._serialize(inp))


class LabController(ModelController):
    def _model(self) -> Type[db.Model]:
        return Lab

    def _serialize(self, obj):
        return {'id': obj.id, 'name': obj.name, 'namespace_prefix': obj.namespace_prefix,
                'description': obj.description, 'docker_image': obj.docker_image_id,
                'docker_image_name': obj.docker_image_name}

    def create(self, name, namespace_prefix, description, docker_image: DockerImage, docker_image_name) -> db.Model:
        return self._create(name=name, namespace_prefix=namespace_prefix, description=description,
                            docker_image=docker_image.id, docker_image_name=docker_image_name)

