"""Entity for Fyta plant image."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.image import ImageEntity, ImageEntityDescription

from .const import DOMAIN
from .coordinator import FytaCoordinator
from .entity import FytaPlantEntity


@dataclass(frozen=True)
class FytaImageEntityDescription(ImageEntityDescription):
    """Describes Fyta image entity."""

    value_fn: Callable[[str | int | float | datetime], str | int | float | datetime] = (
        lambda value: value
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the FYTA plant images."""
    coordinator: FytaCoordinator = hass.data[DOMAIN][entry.entry_id]

    description = FytaImageEntityDescription(
        key="plant_image",
    )

    plant_entities: list[FytaPlantImageEntity] = [
        FytaPlantImageEntity(coordinator, entry, description, plant_id)
        for plant_id in coordinator.fyta.plant_list
        if "plant_origin_path" in coordinator.data[plant_id]
    ]

    async_add_entities(plant_entities)


class FytaPlantImageEntity(FytaPlantEntity, ImageEntity):
    """Represents a Fyta image."""

    entity_description: FytaImageEntityDescription

    def __init__(
        self,
        coordinator: FytaCoordinator,
        entry: ConfigEntry,
        description: FytaImageEntityDescription,
        plant_id: int,
    ) -> None:
        """Initiatlize UniFi Image entity."""
        super().__init__(coordinator, entry, description, plant_id)
        ImageEntity.__init__(self, coordinator.hass)

    @property
    def image_url(self) -> str:
        """Return the image_url for this sensor."""
        image: str = self.plant["plant_origin_path"]
        if image != self._attr_image_url:
            self._attr_image_last_updated = datetime.now()

        return image
