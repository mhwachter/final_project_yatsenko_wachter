from subprocess import check_call


def check_dependency_call(dependency):
    try:
        check_call([dependency, "--version"])
    except FileNotFoundError:
        return False
    else:
        return True


def test_R_installed():
    assert check_dependency_call(
        dependency="R",
    ), "R is not installed. Make sure that it is installed and in the path."


def test_pdflatex_installed():
    assert check_dependency_call(
        dependency="pdflatex",
    ), "pdflatex is not installed. Make sure that it is installed and in the path."


def test_conda_installed():
    assert check_dependency_call(
        dependency="conda",
    ), "conda is not installed. Make sure that it is installed and in the path."


def test_git_installed():
    assert check_dependency_call(
        dependency="git",
    ), "git is not installed. Make sure that it is installed and in the path."
