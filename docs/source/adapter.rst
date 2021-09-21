Adapter
=======

To use this library you need adapter classes. Adapter classes are used to connect the lab orchestrator lib to your database.

Take a look at the controller references to see which adapters you need when you want to use only a few controllers. But to use all features of the library you need to implement all adapters:

* `User Adapter Interface`_
* `Docker Image Adapter Interface`_
* `Lab Adapter Interface`_
* `Lab Instance Adapter Interface`_

.. note::
    When you use **django** there is already one library that contains all adapters to use the lab orchestrator lib with django: `LabOrchestratorLib-DjangoAdapter <https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter>`_. This library also contains an example Django API. On how to use this adapter take a look at the documentation in the link.

.. note::
    The `LabOrchestratorLib-FlaskSQLAlchemyAdapter <https://github.com/LabOrchestrator/LabOrchestratorLib-FlaskSQLAlchemyAdapter>`_ project is not maintained and not working, but if you need an adapter for Flask-SQLAlchemy you can base them on this project.

After implementing the adapters you can create a controller collection by passing instances of the adapters to the ``lab_orchestrator_lib.controllers.controller_collection.create_controller_collection(...)`` function. This function takes all adapters, one api registry and a secret key. More about this is part of :doc:`controller` documentation.

User Adapter Interface
----------------------

.. autoclass:: lab_orchestrator_lib.database.adapter.UserAdapterInterface
    :members:
    :undoc-members:

    .. rubric:: Methods

Docker Image Adapter Interface
------------------------------

.. autoclass:: lab_orchestrator_lib.database.adapter.DockerImageAdapterInterface
    :members:
    :undoc-members:

    .. rubric:: Methods


Lab Adapter Interface
---------------------

.. autoclass:: lab_orchestrator_lib.database.adapter.LabAdapterInterface
    :members:
    :undoc-members:

    .. rubric:: Methods


Lab Instance Adapter Interface
------------------------------

.. autoclass:: lab_orchestrator_lib.database.adapter.LabInstanceAdapterInterface
    :members:
    :undoc-members:

    .. rubric:: Methods
