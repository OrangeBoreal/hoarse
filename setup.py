# Third Party
from setuptools import find_packages, setup

setup(
    name="hoarse",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "kivy==1.9.1",
        "Cython==0.23",
    ],
)
