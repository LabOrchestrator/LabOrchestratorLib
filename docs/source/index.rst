Welcome to LabOrchestratorLib's documentation!
===================================================

**LabOrchestratorLib** is a Python library that contains the core functionality of the lab orchestrator.
It is used in the `LabOrchestrator-API <https://github.com/LabOrchestrator/LabOrchestrator-API>`_.

The Lab Orchestrator is a tool that helps you to orchestrate labs.

A lab is a combination from multiple VMs that share a network. When you start a lab, the VMs are started in Kubernetes in a separate namespace so that you aren't able to connect to labs from other people. You can access the VMs over VNC in the browser with `LabVNC <https://github.com/LabOrchestrator/LabVNC>`_.

You can find the releases of the library at `pypi.org/project/lab-orchestrator-lib/ <https://pypi.org/project/lab-orchestrator-lib/>`_.

Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

.. note::

   This project is under active development.

Contents
--------

.. toctree::
    :maxdepth: 1

    usage
    users
    developer
    api
