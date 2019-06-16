from delira import get_backends
import os


def check_for_environment_variable(variable: str, value: str):
    if variable in os.environ and os.environ[variable] == value:
        return True
    return False


def check_for_backend(backend_name, environment_variable):
    backend_installed = backend_name in get_backends()
    backend_specified = check_for_environment_variable("BACKEND",
                                                       environment_variable)

    return backend_installed and backend_specified


def check_for_torch_backend():
    return check_for_backend("TORCH", "Torch")


def check_for_tf_backend():
    return check_for_backend("TF", "TF")


def check_for_chainer_backend():
    return check_for_backend("CHAINER", "Chainer")


def check_for_sklearn_backend():
    return check_for_backend("SKLEARN", "Sklearn")


def check_for_no_backend():
    # sklearn backend is always installed, so this check is mainly a check if
    # installation was successfull and checks for environment variable
    return check_for_backend("SKLEARN", "None")