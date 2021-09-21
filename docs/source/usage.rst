Usage
=====

.. _installation:

Installation
------------

To use LabOrchestratorLib, first install it using pip:

.. code-block:: console

   (.venv) $ pip3 install lab-orchestrator-lib

Adapter
-------

To use this library you need adapter classes. Adapter classes are used to connect the lab orchestrator lib to your database. How to write them is described in the :doc:`adapter` documentation.

.. note::
    There is already one library that contains all adapters to use the lab orchestrator lib with **django**: `LabOrchestratorLib-DjangoAdapter <https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter>`_. This library also contains an example Django API.

.. note::
    The `LabOrchestratorLib-FlaskSQLAlchemyAdapter <https://github.com/LabOrchestrator/LabOrchestratorLib-FlaskSQLAlchemyAdapter>`_ project is not maintained and not working, but if you need an adapter for Flask-SQLAlchemy you can base them on this project.

Resources
---------

The library contains two types of resources. The first is Kubernetes resources. This type contains ``NetworkPolicy``, ``VirtualMachineInstance`` and ``Namespace`` objects. These are resources from Kubernetes that doesn't need to be saved.

The second type is database resources. They are saved in the database. For every database resource an adapter needs to be added. This type contains ``user``, ``DockerImage``, ``Lab`` and ``LabInstance`` objects.

A ``DockerImage`` is a link to a docker image that contains the VM image. A ``Lab`` contains one or multiple (currently not supported) VMs, each one is linked to a ``DockerImage``. A lab can be started which results into a ``LabInstance``. A ``LabInstance`` contains some ``VirtualMachineInstances`` running in a ``Namespace`` that can be accessed with VNC. The ``LabInstances`` are separated from other ``LabInstances`` with ``NetworkPolicys``.

See more at the :doc:`model` documentation.

Controller
----------

This library makes use of something called controllers. A controller is a class that controls one resource. The controllers can (and should) be used to create, get and update resources.

A controller collection is a collection of all controllers. You can create one with the ``lab_orchestrator_lib.controllers.controller_collection.create_controller_collection(...)`` function. This function takes all adapters, one api registry and a secret key for creating JWT tokens as parameter. The api registry is needed for the Kubernetes controllers and the adapters are injected into the database controllers.

See more at the :doc:`controller` documentation.

Usage
-----

To use this library create a APIRegistry and a controller collection. Than you can use the controllers in the controller collection to create new ``DockerImages``, ``Labs`` and ``LabInstances``.


For example:

>>> from lab_orchestrator_lib.kubernetes.config import get_development_config, get_registry, KubernetesConfig
>>> from lab_orchestrator_lib.kubernetes.api import APIRegistry
>>> from lab_orchestrator_lib.controller.controller_collection import create_controller_collection
>>> secret_key = "secret"
>>> kubernetes_config = get_development_config()
>>> registry = get_registry(kubernetes_config)
>>> user_adapter = UserExampleAdapter()
>>> docker_image_adapter = DockerExamplejangoAdapter()
>>> lab_adapter = LabExampleAdapter()
>>> lab_instance_adapter = LabInstanceExampleAdapter()
>>> cc = create_controller_collection(
>>>     registry=registry,
>>>     user_adapter=user_adapter,
>>>     docker_image_adapter=docker_image_adapter,
>>>     lab_adapter=lab_adapter,
>>>     lab_instance_adapter=lab_instance_adapter,
>>>     secret_key=secret_key,
>>> )
>>> cc.docker_image_ctrl.create("ubuntu", "ubuntu image", "replacewithubuntuimage")
>>> cc.lab_ctrl.create("Example lab", "examplelab", "Example of a lab", "1", "ubuntu")
>>> cc.lab_instance_ctrl("1", "1")
<__main__.LabInstanceKubernetes object at 0x7f7871c76910>
>>> # now the ubuntu image would be started in kubernetes

Examples
--------

An example of the implementation of the adapters and an example of how to used the controllers can be found in the `LabOrchestratorLib-DjangoAdapter <https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter>`_.

