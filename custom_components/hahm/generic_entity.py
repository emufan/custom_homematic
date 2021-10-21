"""Generic entity for the HomematicIP Cloud component."""
from __future__ import annotations

import logging
from typing import Any

from hahomematic.entity import GenericEntity as HMEntity
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import Entity as HAEntity

from .control_unit import Control_Unit

_LOGGER = logging.getLogger(__name__)


class HaHomematicGenericEntity(HAEntity):
    """Representation of the HomematicIP generic entity."""

    def __init__(self, cu: Control_Unit, hm_entity: HMEntity) -> None:
        """Initialize the generic entity."""
        self._cu = cu
        self._hm_entity = hm_entity

        # Marker showing that the Hm device hase been removed.
        self.hm_device_removed = False
        _LOGGER.info("Setting up %s", self.name)

    @property
    def device_class(self) -> str:
        """Return the class of this sensor."""
        return self._hm_entity.device_class

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device specific attributes."""
        return self._hm_entity.device_info

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        # self._hap.hmip_device_by_entity_id[self.entity_id] = self._device
        self._hm_entity.register_update_callback(self._async_device_changed)
        self._cu.add_hm_entity(hm_entity=self._hm_entity)

        # self._device.on_remove(self._async_device_removed)

    @callback
    def _async_device_changed(self, *args, **kwargs) -> None:
        """Handle device state changes."""
        # Don't update disabled entities
        if self.enabled:
            _LOGGER.debug("Event %s (%s)", self.name, self._hm_entity.type)
            self.async_write_ha_state()
        else:
            _LOGGER.debug(
                "Device Changed Event for %s (%s) not fired. Entity is disabled",
                self.name,
                self._hm_entity.device_type,
            )

    async def async_will_remove_from_hass(self) -> None:
        """Run when hmip device will be removed from hass."""

        # Only go further if the device/entity should be removed from registries
        # due to a removal of the HmIP device.

        if self.hmip_device_removed:
            try:
                self._cu.remove_hm_entity(self)
                await self.async_remove_from_registries()
            except KeyError as err:
                _LOGGER.debug("Error removing HM device from registry: %s", err)

    async def async_remove_from_registries(self) -> None:
        """Remove entity/device from registry."""

        # Remove callback from device.
        # self._device.remove_callback(self._async_device_changed)
        # self._device.remove_callback(self._async_device_removed)

        if not self.registry_entry:
            return

        device_id = self.registry_entry.device_id
        if device_id:
            # Remove from device registry.
            device_registry = await dr.async_get_registry(self.hass)
            if device_id in device_registry.devices:
                # This will also remove associated entities from entity registry.
                device_registry.async_remove_device(device_id)
        else:
            # Remove from entity registry.
            # Only relevant for entities that do not belong to a device.
            entity_id = self.registry_entry.entity_id
            if entity_id:
                entity_registry = await er.async_get_registry(self.hass)
                if entity_id in entity_registry.entities:
                    entity_registry.async_remove(entity_id)

    @callback
    def _async_device_removed(self, *args, **kwargs) -> None:
        """Handle hm device removal."""
        # Set marker showing that the Hm device hase been removed.
        # self.hmip_device_removed = True
        # self.hass.async_create_task(self.async_remove(force_remove=True))

    @property
    def name(self) -> str:
        """Return the name of the generic entity."""

        return self._hm_entity.name

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # TODO
        return True

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._hm_entity.unique_id

    # @property
    # def icon(self) -> str | None:
    #     """Return the icon."""
    #     return self._hm_entity.icon

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        state_attr = {}

        return state_attr
