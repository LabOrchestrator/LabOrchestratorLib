Models
======

The library contains two types of resources. The first is Kubernetes resources. This type contains ``NetworkPolicy``, ``VirtualMachineInstance`` and ``Namespace`` objects. These are resources from Kubernetes that doesn't need to be saved.

The second type is database resources. They are saved in the database. For every database resource an adapter needs to be added. This type contains ``user``, ``DockerImage``, ``LabDockerImage``, ``Lab`` and ``LabInstance`` objects.

Database resources:

* `User`_
* `Docker Image`_
* `Lab Docker Image`_
* `Lab`_
* `Lab Instance`_
* `Lab Instance Kubernetes`_

Abstract resources:

* `Model`_


User
----

.. autoclass:: lab_orchestrator_lib.model.model.User
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods


Docker Image
------------

.. autoclass:: lab_orchestrator_lib.model.model.DockerImage
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods


Lab Docker Image
----------------

.. autoclass:: lab_orchestrator_lib.model.model.LabDockerImage
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods


Lab
---

.. autoclass:: lab_orchestrator_lib.model.model.Lab
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods


Lab Instance
------------

.. autoclass:: lab_orchestrator_lib.model.model.LabInstance
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods


Lab Instance Kubernetes
-----------------------

.. autoclass:: lab_orchestrator_lib.model.model.LabInstanceKubernetes
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods


Model
-----

This class should not be used. It's just a abstract base class used for all models.

.. autoclass:: lab_orchestrator_lib.model.model.Model
    :show-inheritance:
    :special-members: __init__
    :undoc-members:

    .. rubric:: Methods
