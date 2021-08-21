from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lab-orchestrator-lib",
    version="0.0.2",
    author="Marco Schlicht",
    author_email="git@privacymail.dev",
    description="Manages Labs in your Kubernetes Cluster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LabOrchestrator/LabOrchestratorLib",
    license="MPL",
    project_urls={
        "Bug Tracker": "https://github.com/LabOrchestrator/LabOrchestratorLib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['PyYAML~=5.4.1', 'requests~=2.26.0']
)
