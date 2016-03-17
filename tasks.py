from invoke import run, task

@task
def lint():
    """
    Make all kinds of checks on the code to see if it's pretty
    """
    run("pep8 .", warn=True)
    run("pylint hoarse tasks.py", warn=True)
    run("isort -c", warn=True)

@task
def isort():
    """
    Sorts all the imports
    """
    run("isort .")

@task
def tests():
    """
    Launches tests suite
    """
    run("python -m unittest tests")
