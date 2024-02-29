"""Summary binary data from FYTA."""
from __future__ import annotations

from typing import Final

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FytaCoordinator
from .entity import FytaCoordinatorEntity, FytaPlantEntity


BINARY_SENSORS: Final[list[BinarySensorEntityDescription]] = [
    BinarySensorEntityDescription(
        key="online",
        translation_key="online",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BinarySensorEntityDescription(
        key="battery_status",
        translation_key="battery_status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Nextcloud binary sensors."""
    coordinator: FytaCoordinator = hass.data[DOMAIN][entry.entry_id]

    plant_entities: list[CoordinatorEntity] = [
        FytaCoordinatorBinarySensor(coordinator, entry, sensor)
        for sensor in BINARY_SENSORS
        if sensor.key in coordinator.data
    ]

    plant_entities.extend(
        FytaPlantBinarySensor(coordinator, entry, sensor, plant_id)
        for plant_id in coordinator.fyta.plant_list
        for sensor in BINARY_SENSORS
        if sensor.key in coordinator.data[plant_id]
    )

    async_add_entities(plant_entities)


class FytaCoordinatorBinarySensor(FytaCoordinatorEntity, BinarySensorEntity):
    """Represents a Fyta Coordinator binary sensor."""

    entity_description: BinarySensorEntityDescription

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        val = self.coordinator.data[self.entity_description.key]
        return val is True or val == "yes"


class FytaPlantBinarySensor(FytaPlantEntity, BinarySensorEntity):
    """Represents a Fyta plant binary sensor."""

    entity_description: BinarySensorEntityDescription

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        val = self.plant[self.entity_description.key]
        return val is True or val == "yes"
