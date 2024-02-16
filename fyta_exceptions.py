"""Asynchronous Python client for FYTA."""


class FytaError(Exception):
    """Generic exception."""


class FytaConnectionError(FytaError):
    """Analytics connection exception."""

class FytaAuthentificationError(FytaError):
    """Fyta Password exception (wrong password)."""

class FytaPasswordError(FytaError):
    """Fyta Password exception (wrong password)."""

class FytaPlantError(FytaError):
    """Fyta exception in getting plants."""
