Controller
==========

This library makes use of something called controllers. A controller is a class that controls one resource. The controllers can (and should) be used to create, get and update resources.

Available controllers are:

* `User Controller`_
* `Namespace Controller`_
* `Network Policy Controller`_
* `Docker Image Controller`_
* `Lab Docker Image Controller`_
* `Lab Controller`_
* `Virtual Machine Instance Controller`_
* `Lab Instance Controller`_

In addition to this:

* `Controller Collection`_
* `Create Controller Collection`_

Abstract controllers (internal only):

* `Adapter Controller`_
* `Kubernetes Controller`_
* `Namespaced Controller`_
* `Not Namespaced Controller`_

.. note::
    Please read the class documentations carefully.


User Controller
---------------

.. autoclass:: lab_orchestrator_lib.controller.controller.UserController
    :special-members: __init__
    :show-inheritance:
    :members:
    :undoc-members:

    .. rubric:: Methods


Namespace Controller
--------------------

.. autoclass:: lab_orchestrator_lib.controller.controller.NamespaceController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:
    :exclude-members: template_file

    .. rubric:: Methods


Network Policy Controller
-------------------------

.. autoclass:: lab_orchestrator_lib.controller.controller.NetworkPolicyController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:
    :exclude-members: template_file

    .. rubric:: Methods


Docker Image Controller
-----------------------

.. autoclass:: lab_orchestrator_lib.controller.controller.DockerImageController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

    .. rubric:: Methods


Lab Docker Image Controller
---------------------------

.. autoclass:: lab_orchestrator_lib.controller.controller.LabDockerImageController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

    .. rubric:: Methods


Lab Controller
--------------

.. autoclass:: lab_orchestrator_lib.controller.controller.LabController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

    .. rubric:: Methods


Virtual Machine Instance Controller
-----------------------------------

.. autoclass:: lab_orchestrator_lib.controller.controller.VirtualMachineInstanceController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:
    :exclude-members: template_file

    .. rubric:: Methods


Lab Instance Controller
-----------------------

.. autoclass:: lab_orchestrator_lib.controller.controller.LabInstanceController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

    .. rubric:: Methods



Controller Collection
---------------------

A controller collection is a collection of all controllers. You can create one with the ``lab_orchestrator_lib.controllers.controller_collection.create_controller_collection(...)`` function. This function takes all adapters, one api registry and a secret key for creating JWT tokens as parameter. The api registry is needed for the Kubernetes controllers and the adapters are injected into the database controllers.

.. autoclass:: lab_orchestrator_lib.controller.controller_collection.ControllerCollection
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:


Create Controller Collection
----------------------------

This method could be used to create all controllers at once.

.. autofunction:: lab_orchestrator_lib.controller.controller_collection.create_controller_collection


Adapter Controller
------------------

.. autoclass:: lab_orchestrator_lib.controller.adapter_controller.AdapterController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:


Kubernetes Controller
---------------------

.. autoclass:: lab_orchestrator_lib.controller.kubernetes_controller.KubernetesController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

Namespaced Controller
---------------------

.. autoclass:: lab_orchestrator_lib.controller.kubernetes_controller.NamespacedController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:


Not Namespaced Controller
-------------------------

.. autoclass:: lab_orchestrator_lib.controller.kubernetes_controller.NotNamespacedController
    :special-members: __init__
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:


