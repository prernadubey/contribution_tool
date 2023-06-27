import json
import logging
import typing as t


def get_clean_error_message(msg: str) -> str:
    """Returns msg that is cleaned without slashes, double space and new line.

    Args:
          msg (str): message to be cleaned

    Returns:
          msg (str): clean message
    """
    return msg.replace(" ", "").replace("\\n", "").replace("\\", "")


def get_traceback_struct(exc: Exception) -> t.List[t.Dict[t.Any, t.Any]]:
    traceback_struct = []
    tb = exc.__traceback__
    while tb is not None:
        traceback_struct.append(
            {
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "ineno": tb.tb_lineno,
            }
        )
        tb = tb.tb_next
    return traceback_struct


class BaseAppException(Exception):
    """Base class for all the errors"""

    _logger = logging.getLogger("ExceptionLogger")

    def __init__(
        self, message: str, extra: t.Optional[t.Mapping[str, t.Optional[str]]] = None
    ) -> None:
        self.message = message
        self.extra = extra or {}

        self._logger.error(message, extra=extra)

    def __str__(self):
        return get_clean_error_message(
            json.dumps(
                {self.__class__.__name__: {**self.extra, "message": self.message}}
            )
        )


class RepositoryBaseException(BaseAppException):
    """Base class for all the errors related to repository processing"""


class RepositoryExternalException(RepositoryBaseException):
    """Class representing external errors during repository processing"""


class RepositoryProcessingException(RepositoryBaseException):
    """Class representing internal processing errors during repository processing"""


class DBException(BaseAppException):
    """Base class for all the errors related to databse communication"""


class DBProcessingException(BaseAppException):
    """Class representing external errors during database query processing"""


class DBExternalException(BaseAppException):
    """Closs representing external errors during database communication"""


class ConfigurationException(BaseAppException):
    """Base class for all the errors related to configuration"""


class UseCaseProcessingException(BaseAppException):
    """Class representing errors during use case processing"""
