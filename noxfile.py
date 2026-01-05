import nox

SRC = "src/montecarlo_pi"
TESTS = "tests"

@nox.session(python=False)
def tests(session):
    """Run pytest on the tests folder."""
    session.log("=== Running pytest ===")
    # Use Poetry-managed virtualenv
    session.run("poetry", "run", "pytest", TESTS, external=True)

@nox.session(python=False)
def lint(session):
    """Run pylint on the source folder."""
    session.log("=== Running pylint ===")
    session.run("poetry", "run", "pylint", SRC, external=True)

@nox.session(python=False)
def check(session):
    """Run tests and lint sequentially; fail if either fails."""
    session.notify("tests")
    session.notify("lint")
