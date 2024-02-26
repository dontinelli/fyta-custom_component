"""Config flow for FYTA integration."""
from __future__ import annotations

import logging
from .fyta_exceptions import (
    FytaConnectionError,
    FytaAuthentificationError,
    FytaPasswordError,
)
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant

from .const import DOMAIN

from .fyta_connector import FytaConnector


_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    access_token = data.get("access_token", "")
    expiration = data.get("expiration", "")

    fyta = FytaConnector(data[CONF_USERNAME], data[CONF_PASSWORD], access_token, expiration)

    result = await fyta.test_connection()
    if not result:
        raise CannotConnect

    try:
        await fyta.login()
    except FytaConnectionError as ex:
        raise CannotConnect from ex
    except FytaAuthentificationError as ex:
        raise InvalidAuth from ex
    except FytaPasswordError as ex:
        raise InvalidPassword from ex

    return {"title": data[CONF_USERNAME]}


class FytaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fyta."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._errors: dict = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors[CONF_USERNAME] = "Athentication error"
                errors[CONF_PASSWORD] = "Athentication error"
            except InvalidPassword:
                errors[CONF_PASSWORD] = "Athentication error"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there are invalid credentials."""

class InvalidPassword(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid password."""

