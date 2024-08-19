"""Entities for FYTA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fyta_cli.fyta_models import Plant

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FytaCoordinator

if TYPE_CHECKING:
    from . import FytaConfigEntry

class FytaCoordinatorEntity(CoordinatorEntity[FytaCoordinator]):
    """Base Fyta Coordinator entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: FytaCoordinator,
        entry: FytaConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the FytaCoordinator sensor."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{entry.entry_id}-{description.key}"
        self._attr_device_info = DeviceInfo(
            manufacturer="Fyta",
            model="Controller",
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Fyta Coordinator ({self.coordinator.fyta.email})",
        )

        self.entity_description = description


class FytaPlantEntity(CoordinatorEntity[FytaCoordinator]):
    """Base Fyta Plant entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: FytaCoordinator,
        entry: FytaConfigEntry,
        description: SensorEntityDescription,
        plant_id: int,
    ) -> None:
        """Initialize the Fyta sensor."""
        super().__init__(coordinator)

        self.plant_id = plant_id
        self._attr_unique_id = f"{entry.entry_id}-{plant_id}-{description.key}"
        self._attr_device_info = DeviceInfo(
            manufacturer="Fyta",
            model="Plant",
            identifiers={(DOMAIN, f"{entry.entry_id}-{plant_id}")},
            name=self.plant.name,
            via_device=(DOMAIN, entry.entry_id),
            sw_version=self.plant.sw_version,
        )
        self.entity_description = description

    @property
    def plant(self) -> Plant:
        """Get plant data."""
        return self.coordinator.data[self.plant_id]

    @property
    def available(self) -> bool:
        """Test if entity is available."""
        return super().available and self.plant_id in self.coordinator.data
