"""Initialization of FYTA integration."""
from __future__ import annotations

from .fyta_connector import FytaConnector

import logging
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import FytaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = (Platform.SENSOR, Platform.BINARY_SENSOR)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the FYTA integration.

    Args:
        hass: HomeAssistant:
        entry: ConfigEntry:

    Returns: bool:

    """
    #_LOGGER.exception(f"async_setup_entry {entry.entry_id}")
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    access_token = entry.data.get("access_token", "")
    expiration = (entry.data["expiration"] if "expiration" in entry.data else datetime.now())

    fyta = FytaConnector(username, password, access_token, expiration)

    coordinator = FytaCoordinator(hass, fyta, entry)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    if access_token == "" or expiration < datetime.now():
        await fyta.login()

    await coordinator._async_update_data()
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_remove_config_entry_device(hass, config_entry, device_entry) -> bool:
    """Delete device if no entities."""
    if device_entry.model == "Controller":
        _LOGGER.error(
            "You cannot delete the Fyta Controller device via the device delete method. %s",
            "Please remove the integration instead.",
        )
        return False
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry from Home Assistant."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
