from setuptools import setup , find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

    # Jese pip install pandas se library import hojati hai wese hi hum khudka setup bana rahe hai taki pip install mlops se hamara project install hojaye pc mai

    # Command to run setup.py is pip install -e .

setup(
    name="mlops",
    version="0.1",
    author="Vedant Jain",
    description="MLOPS Project",
    packages = find_packages(), # it will treat src folder as a package because it has__init__.py file in it
    install_requires = requirements,
    python_requires = ">=3.7"
)