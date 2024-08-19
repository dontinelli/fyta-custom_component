"""Entity for Fyta plant image."""
from __future__ import annotations

from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.image import ImageEntity, ImageEntityDescription

from . import FytaConfigEntry
from .coordinator import FytaCoordinator
from .entity import FytaPlantEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: FytaConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the FYTA plant images."""
    coordinator: FytaCoordinator = entry.runtime_data

    description = ImageEntityDescription(
        key="plant_image",
    )

    plant_entities: list[FytaPlantImageEntity] = [
        FytaPlantImageEntity(coordinator, entry, description, plant_id)
        for plant_id in coordinator.fyta.plant_list
        if "plant_origin_path" in dir(coordinator.data[plant_id])
    ]

    async_add_entities(plant_entities)


class FytaPlantImageEntity(FytaPlantEntity, ImageEntity):
    """Represents a Fyta image."""

    entity_description: ImageEntityDescription

    def __init__(
        self,
        coordinator: FytaCoordinator,
        entry: ConfigEntry,
        description: ImageEntityDescription,
        plant_id: int,
    ) -> None:
        """Initiatlize UniFi Image entity."""
        super().__init__(coordinator, entry, description, plant_id)
        ImageEntity.__init__(self, coordinator.hass)

    @property
    def image_url(self) -> str:
        """Return the image_url for this sensor."""
        image: str = self.plant.plant_origin_path
        if image != self._attr_image_url:
            self._attr_image_last_updated = datetime.now()

        return image
