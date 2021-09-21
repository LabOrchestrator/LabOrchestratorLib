# Lab Orchestrator Lib

This package contains the lab orchestrator library.

## Installation

- `pip3 install lab-orchestrator-lib`

## Documentation

Check out the developer documentation at [laborchestratorlib.readthedocs.io](https://laborchestratorlib.readthedocs.io/en/latest/).

## Adapter

To use this library you need adapter classes. Adapter classes are used to connect the lab orchestrator lib to your database. How to write them is described in the [adapter documentation](https://laborchestratorlib.readthedocs.io/en/latest/adapters.html)

**Adapter Libraries:**

There is already one library that contains all adapters to use the lab orchestrator lib with **django**: [LabOrchestratorLib-DjangoAdapter](https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter). This library also contains an example Django API.

The [LabOrchestratorLib-FlaskSQLAlchemyAdapter](https://github.com/LabOrchestrator/LabOrchestratorLib-FlaskSQLAlchemyAdapter) project is not maintained and not working, but if you need an adapter for Flask-SQLAlchemy you can base them on this project.

## Resources

The library contains two types of resources. The first is Kubernetes resources. This type contains `NetworkPolicy`, `VirtualMachineInstance` and `Namespace` objects. These are resources from Kubernetes that doesn't need to be saved.

The second type is database resources. They are saved in the database. For every database resource an adapter needs to be added. This type contains `user`, `DockerImage`, `Lab` and `LabInstance` objects.

A `DockerImage` is a link to a docker image that contains the VM image. A `Lab` contains one or multiple (currently not supported) VMs, each one is linked to a `DockerImage`. A lab can be started which results into a `LabInstance`. A `LabInstance` contains some `VirtualMachineInstance`s running in a `Namespace` that can be accessed with VNC. The `LabInstances` are separated from other `LabInstances` with `NetworkPolicy`s.

## Controller

This library makes use of something called controllers. A controller is a class that controls one resource. The controllers can (and should) be used to create, get and update resources.

A controller collection is a collection of all controllers. You can create one with the `lab_orchestrator_lib.controllers.controller_collection.create_controller_collection(...)` function. This function takes all adapters, one api registry and a secret key for creating JWT tokens as parameter. The api registry is needed for the Kubernetes controllers and the adapters are injected into the database controllers.

## Usage

To use this library create a APIRegistry and a controller collection. Than you can use the controllers in the controller collection to create new `DockerImage`s, `Lab`s and `LabInstance`s.

For detailed information take a look at the developer documentation at [laborchestratorlib.readthedocs.io](https://laborchestratorlib.readthedocs.io/en/latest/).

## Examples

An example of the implementation of the adapters and an example of how to used the controllers can be found in the [LabOrchestratorLib-DjangoAdapter](https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter).

## Contributing

### Issues

Feel free to open [issues](https://github.com/LabOrchestrator/LabOrchestratorLib/issues).

### Project Structure

The `src` folder contains the source code of the library. The `tests` folder contains the test cases. There is a makefile that contains some shortcuts for example to run the test cases and to make a release. Run `make help` to see all targets. The `docs` folder contains rst docs that are used in [read the docs](https://laborchestratorlib.readthedocs.io/en/latest/). Kubernetes yaml templates are placed in `src/lab_orchestrator_lib/templates/`.

### Developer Dependencies

- Python 3.8
- Make
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`

### Releases

Your part:

1. Create branch for your feature (`issue/ISSUE_ID-SHORT_DESCRIPTION`)
2. Code
3. Make sure test cases are running and add new ones for your feature
4. Create MR into master
5. Increase version number in `src/lab_orchestrator_lib/__init__.py` (semantic versioning)

Admin part:

1. Check and accept MR
2. Merge MR
3. Run `make release`

### Docs

To generate the docs run: `cd docs && make html`.
