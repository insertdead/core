"""Support for Rituals Perfume Genie numbers."""
from __future__ import annotations

from pyrituals import Diffuser

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RitualsDataUpdateCoordinator
from .const import ATTRIBUTES, COORDINATORS, DEVICES, DOMAIN, SPEED
from .entity import DiffuserEntity

MIN_PERFUME_AMOUNT = 1
MAX_PERFUME_AMOUNT = 3

PERFUME_AMOUNT_SUFFIX = " Perfume Amount"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the diffuser numbers."""
    diffusers = hass.data[DOMAIN][config_entry.entry_id][DEVICES]
    coordinators = hass.data[DOMAIN][config_entry.entry_id][COORDINATORS]
    entities: list[DiffuserEntity] = []
    for hublot, diffuser in diffusers.items():
        coordinator = coordinators[hublot]
        entities.append(DiffuserPerfumeAmount(diffuser, coordinator))

    async_add_entities(entities)


class DiffuserPerfumeAmount(DiffuserEntity, NumberEntity):
    """Representation of a diffuser perfume amount number."""

    def __init__(
        self, diffuser: Diffuser, coordinator: RitualsDataUpdateCoordinator
    ) -> None:
        """Initialize the diffuser perfume amount number."""
        super().__init__(diffuser, coordinator, PERFUME_AMOUNT_SUFFIX)

    @property
    def icon(self) -> str:
        """Return the icon of the perfume amount entity."""
        return "mdi:gauge"

    @property
    def value(self) -> int:
        """Return the current perfume amount."""
        return self._diffuser.hub_data[ATTRIBUTES][SPEED]

    @property
    def min_value(self) -> int:
        """Return the minimum perfume amount."""
        return MIN_PERFUME_AMOUNT

    @property
    def max_value(self) -> int:
        """Return the maximum perfume amount."""
        return MAX_PERFUME_AMOUNT

    async def async_set_value(self, value: float) -> None:
        """Set the perfume amount."""
        if value.is_integer() and MIN_PERFUME_AMOUNT <= value <= MAX_PERFUME_AMOUNT:
            await self._diffuser.set_perfume_amount(int(value))
        else:
            raise ValueError(
                f"Can't set the perfume amount to {value}. "
                f"Perfume amount must be an integer between {self.min_value} and {self.max_value}, inclusive"
            )
