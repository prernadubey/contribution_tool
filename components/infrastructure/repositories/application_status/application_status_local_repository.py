import logging
import typing as t
from pathlib import Path

import aiofiles
import aiofiles.os

from components.domain.application_status import ApplicationStatus
from components.infrastructure.repositories.application_status.interface import (
    ApplicationRepositoryProtocol,
)
from components.settings import get_settings

SETTINGS = get_settings()
_logger = logging.getLogger(__name__)


class ApplicationLocalRepository(ApplicationRepositoryProtocol):
    def __init__(self, maintenance_mode_status_filename: str):
        self.maintenance_mode_status_filename = maintenance_mode_status_filename

    async def get_application_status(self) -> ApplicationStatus:
        _maintenance_mode = await self._get_maintenance_mode()
        application_status = ApplicationStatus(
            version=SETTINGS.service_version,
            app_name=SETTINGS.service_name,
            maintenance_mode=_maintenance_mode,
        )

        return application_status

    @staticmethod
    async def _check_path_exists(path: t.Union[Path, str]) -> bool:
        try:
            await aiofiles.os.stat(str(path))
            return True
        except FileNotFoundError as e:
            _logger.warning(e)
        except OSError as e:
            _logger.error(e)
            raise
        except ValueError as e:
            _logger.warning(e)
        return False

    @staticmethod
    async def _create_empty_file(path: t.Union[Path, str]):
        handle = None
        try:
            handle = await aiofiles.open(path, mode="x")
        finally:
            if handle:
                await handle.close()

        _logger.debug(f"File {path} created.")

    @staticmethod
    async def _remove_file(path) -> None:
        try:
            await aiofiles.os.remove(path)
        except IOError as e:
            _logger.error(f"Cannot remove file {path}: {e}")

    async def _get_maintenance_mode(self) -> bool:
        if await ApplicationLocalRepository._check_path_exists(
            self.maintenance_mode_status_filename
        ):
            _logger.debug("Maintenance mode is turned on.")
            return True

        return False

    async def turn_on_maintenance_mode(self) -> None:
        if await ApplicationLocalRepository._check_path_exists(
            self.maintenance_mode_status_filename
        ):
            _logger.debug(
                f"Maintenance mode is turned on. File {self.maintenance_mode_status_filename} "
                "already exists."
            )
            return
        await ApplicationLocalRepository._create_empty_file(
            self.maintenance_mode_status_filename
        )

    async def turn_off_maintenance_mode(self) -> None:
        if not await ApplicationLocalRepository._check_path_exists(
            self.maintenance_mode_status_filename
        ):
            _logger.debug(
                f"Maintenance mode is turned off. File {self.maintenance_mode_status_filename} "
                "does not exists."
            )
            return
        await ApplicationLocalRepository._remove_file(
            self.maintenance_mode_status_filename
        )
