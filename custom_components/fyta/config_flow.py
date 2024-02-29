"""Config flow for FYTA integration."""
from __future__ import annotations

import logging
from typing import Any

from fyta_cli.fyta_connector import FytaConnector
from fyta_cli.fyta_exceptions import (
    FytaAuthentificationError,
    FytaConnectionError,
    FytaPasswordError,
)
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


DATA_SCHEMA = vol.Schema(
    {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
)


class FytaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fyta."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        errors = {}
        if user_input:
            self._async_abort_entries_match({CONF_USERNAME: user_input[CONF_USERNAME]})

            fyta = FytaConnector(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            credentials: dict[str, str | datetime] = {}

            try:
                credentials = await fyta.login()
                await fyta.client.close()
            except FytaConnectionError:
                errors["base"] = "cannot_connect"
            except FytaAuthentificationError:
                errors["base"] = "invalid_auth"
            except FytaPasswordError:
                errors["base"] = "invalid_auth"
                errors[CONF_PASSWORD] = "password_error"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                user_input |= credentials

                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """Handle flow upon an API authentication error."""
        self._entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reauthorization flow."""
        errors = {}
        assert self._entry is not None

        if user_input:

            fyta = FytaConnector(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            credentials: dict[str, str | datetime] = {}

            try:
                credentials = await fyta.login()
                await fyta.client.close()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
                errors[CONF_USERNAME] = "auth_error"
                errors[CONF_PASSWORD] = "auth_error"
            except InvalidPassword:
                errors["base"] = "invalid_auth"
                errors[CONF_PASSWORD] = "password_error"
            else:
                self.hass.config_entries.async_update_entry(
                    self._entry,
                    data={**self._entry.data, **user_input},
                )
                await self.hass.config_entries.async_reload(self._entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        data_schema = self.add_suggested_values_to_schema(
            DATA_SCHEMA,
            {CONF_USERNAME: self._entry.data[CONF_USERNAME], **(user_input or {})},
        )
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=data_schema,
            description_placeholders={"FYTA username": self._entry.data[CONF_USERNAME]},
            errors=errors,
        )
