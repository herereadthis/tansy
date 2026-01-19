import nox

SRC = "src/montecarlo_pi"
TESTS = "tests"

@nox.session(python=False)
def tests(session):
    """Run pytest with coverage."""
    session.log("=== Running pytest with coverage ===")
    session.run(
        "poetry",
        "run",
        "pytest",
        TESTS,
        "--cov=montecarlo_pi",
        "--cov-report=term-missing",
        external=True,
    )

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

@nox.session
def dev(session):
    """Run local FastAPI development server"""
    session.run("uvicorn", "montecarlo_pi.api.main:app", "--port", "5101", "--reload")
