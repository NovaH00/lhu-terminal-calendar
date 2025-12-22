import os
from typing import TypeVar

class EnvironmentVariableMissing(Exception):
    pass

class FailedToCastType(Exception):
    pass

T = TypeVar("T", str, float, int, bool)
def get_env(
    key: str,
    cast_type: type[T] = str,
) -> T:
    """
    Retrieve an environment variable and cast its value to the specified type.

    This function reads the environment variable identified by ``key`` and
    attempts to convert its string value into the type provided via
    ``cast_type``. The return type is inferred from ``cast_type``.

    Args:
        key:
            The name of the environment variable to retrieve.
        cast_type:
            A type used to cast the environment variable value.
            Supported types are ``str``, ``int``, ``float``, and ``bool``.
            Defaults to ``str``.

    Returns:
        The value of the environment variable, cast to ``cast_type``.

    Raises:
        EnvironmentVariableMissing:
            If the environment variable does not exist.
        FailedToCastType:
            If the value cannot be cast to the specified type.

    Examples:
        >>> get_env("APP_NAME")
        'my_app'

        >>> get_env("PORT", int)
        8080

        >>> get_env("DEBUG", bool)
        True
    """   
    env = os.getenv(key)

    if env is None:
        raise EnvironmentVariableMissing(
            f"The environment variable {key} does not exist"
        )

    try:
        return cast_type(env)
    except Exception:
        raise FailedToCastType(
            f"Failed to cast variable {key} to `{cast_type.__name__}`"
        )
