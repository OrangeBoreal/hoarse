# Standard Library
import sys

# Third Party
from invoke import run, task


@task
def lint():
    """
    Make all kinds of checks on the code to see if it's pretty
    """
    print("Pep 8")
    pep8_cmd = run("pep8 --max-line-length=120 .", warn=True)
    print("PyLint")
    pylint_cmd = run("pylint hoarse tasks.py", warn=True)
    print("ISort")
    isort_cmd = run("isort -c", warn=True)

    sys.exit(max(command.exited for command in [pep8_cmd, pylint_cmd, isort_cmd]))


@task
def isort():
    """
    Sorts all the imports
    """
    run("isort -rc .")


@task
def tests():
    """
    Launches tests suite
    """
    run("python -m unittest tests")
