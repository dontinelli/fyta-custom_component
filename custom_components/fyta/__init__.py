"""Initialization of FYTA integration."""
from __future__ import annotations

from datetime import datetime
import logging

from fyta_cli.fyta_connector import FytaConnector

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import async_get_time_zone

from .const import CONF_EXPIRATION, DOMAIN
from .coordinator import FytaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.IMAGE
]
type FytaConfigEntry = ConfigEntry[FytaCoordinator]

async def async_setup_entry(hass: HomeAssistant, entry: FytaConfigEntry) -> bool:
    """Set up the FYTA integration.

    Args:
        hass: HomeAssistant:
        entry: ConfigEntry:

    Returns: bool:

    """
    tz: str = hass.config.time_zone

    username: str = entry.data[CONF_USERNAME]
    password: str = entry.data[CONF_PASSWORD]
    access_token: str = entry.data.get("access_token", "")
    expiration: datetime = datetime.fromisoformat(
        entry.data[CONF_EXPIRATION]
    ).astimezone(await async_get_time_zone(tz))

    fyta = FytaConnector(username, password, access_token, expiration, tz)

    coordinator = FytaCoordinator(hass, fyta)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_remove_config_entry_device(hass: HomeAssistant, config_entry:FytaConfigEntry, device_entry) -> bool:
    """Delete device if no entities."""
    if device_entry.model == "Controller":
        _LOGGER.error(
            "You cannot delete the Fyta Controller device via the device delete method. %s",
            "Please remove the integration instead.",
        )
        return False
    return True


async def async_unload_entry(hass: HomeAssistant, entry: FytaConfigEntry) -> bool:
    """Unload Fyta entity."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version > 1:
        # This means the user has downgraded from a future version
        return False

    if config_entry.version == 1:
        if config_entry.minor_version < 2:
            new = {**config_entry.data}
            fyta = FytaConnector(
                config_entry.data[CONF_USERNAME], config_entry.data[CONF_PASSWORD]
            )
            credentials = await fyta.login()
            await fyta.client.close()

            new[CONF_ACCESS_TOKEN] = credentials.access_token
            new[CONF_EXPIRATION] = credentials.expiration.isoformat()

            hass.config_entries.async_update_entry(
                config_entry, data=new, minor_version=2, version=1
            )

    _LOGGER.debug(
        "Migration to version %s.%s successful",
        config_entry.version,
        config_entry.minor_version,
    )

    return True