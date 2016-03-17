from setuptools import setup, find_packages

setup(
    name="hoarse",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "kivy==1.9.1",
        "Cython==0.23",
    ]
)
