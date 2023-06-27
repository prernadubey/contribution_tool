import logging
import os
from enum import Enum

from pydantic import BaseSettings

from components.utils import singleton

SETTINGS_ENVIRONMENT_VARIABLE = "ENV"


class Environment(str, Enum):
    prod = "prod"
    dev = "dev"
    testing = "testing"
    local = "local"


DEFAULT_ENVIRONMENT = Environment.local


class Settings(BaseSettings):
    """
    Application settings object.

    Defines application specific settings and default values. Default values can
    overridden by modifying the environment specific settings objects below.
    """

    # Application
    debug: bool = False
    testing: bool = False
    log_level: int = logging.DEBUG

    maintenance_mode_status_filename: str = "/tmp/app_maintenance_mode"  # nosec
    service_version: str = "no-version"
    service_name: str = "compensation-tool-be"

    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@singleton
def get_production_settings() -> Settings:
    """
    Settings for the production environment.
    Used when the application is deployed to prod.
    """
    return Settings(  # type: ignore
        log_level=logging.INFO,
    )


@singleton
def get_dev_settings() -> Settings:
    """
    Settings for the production environment.
    Used when the application is deployed to prod.
    """

    return Settings(  # type: ignore
        log_level=logging.INFO,
    )


@singleton
def get_local_dev_settings() -> Settings:
    """
    Settings for the production environment.
    Used when the application is deployed to prod.
    """
    return Settings(  # type: ignore
        debug=True,
        log_level=logging.DEBUG,
    )


@singleton
def get_testing_settings() -> Settings:
    """
    Settings for the production environment.
    Used when the application is deployed to prod.
    """
    return Settings(  # type: ignore
        debug=True,
        log_level=logging.DEBUG,
    )


def get_settings() -> Settings:
    env_value = os.environ.get(SETTINGS_ENVIRONMENT_VARIABLE)
    if env_value is None:
        return get_local_dev_settings()

    env = Environment(env_value)

    if env is Environment.testing:
        return get_testing_settings()
    elif env is Environment.dev:
        return get_dev_settings()
    elif env is Environment.prod:
        return get_production_settings()

    return get_local_dev_settings()
