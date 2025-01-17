"""binary_switch for Homematic(IP) Local."""
from __future__ import annotations

import logging
from typing import Any, Union

from hahomematic.const import HmPlatform
from hahomematic.devices.switch import CeSwitch
from hahomematic.platforms.switch import HmSwitch, HmSysvarSwitch
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_platform
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .control_unit import ControlUnit
from .generic_entity import (
    HaHomematicGenericRestoreEntity,
    HaHomematicGenericSysvarEntity,
)

_LOGGER = logging.getLogger(__name__)
ATTR_ON_TIME = "on_time"
ATTR_CHANNEL_STATE = "channel_state"
SERVICE_SWITCH_SET_ON_TIME = "switch_set_on_time"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Homematic(IP) Local switch platform."""
    control_unit: ControlUnit = hass.data[DOMAIN][config_entry.entry_id]

    @callback
    def async_add_switch(args: Any) -> None:
        """Add switch from Homematic(IP) Local."""
        entities: list[HaHomematicGenericRestoreEntity] = []

        for hm_entity in args:
            entities.append(HaHomematicSwitch(control_unit, hm_entity))

        if entities:
            async_add_entities(entities)

    @callback
    def async_add_hub_switch(args: Any) -> None:
        """Add sysvar switch from Homematic(IP) Local."""

        entities = []

        for hm_entity in args:
            entities.append(HaHomematicSysvarSwitch(control_unit, hm_entity))

        if entities:
            async_add_entities(entities)

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            control_unit.async_signal_new_hm_entity(
                config_entry.entry_id, HmPlatform.SWITCH
            ),
            async_add_switch,
        )
    )
    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            control_unit.async_signal_new_hm_entity(
                config_entry.entry_id, HmPlatform.HUB_SWITCH
            ),
            async_add_hub_switch,
        )
    )

    async_add_switch(
        control_unit.async_get_new_hm_entities_by_platform(platform=HmPlatform.SWITCH)
    )

    async_add_hub_switch(
        control_unit.async_get_new_hm_entities_by_platform(
            platform=HmPlatform.HUB_SWITCH
        )
    )

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SWITCH_SET_ON_TIME,
        {
            vol.Required(ATTR_ON_TIME): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=8580000)
            ),
        },
        "async_set_on_time",
    )


class HaHomematicSwitch(
    HaHomematicGenericRestoreEntity[Union[CeSwitch, HmSwitch]], SwitchEntity
):
    """Representation of the HomematicIP switch entity."""

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the generic entity."""
        attributes = super().extra_state_attributes
        if isinstance(self._hm_entity, CeSwitch):
            if (
                self._hm_entity.channel_value
                and self._hm_entity.value != self._hm_entity.channel_value
            ):
                attributes[ATTR_CHANNEL_STATE] = self._hm_entity.channel_value
        return attributes

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        if self._hm_entity.is_valid:
            return self._hm_entity.value is True
        if self.is_restored:
            if (restored_state := self._restored_state.state) not in (  # type: ignore[union-attr]
                STATE_UNKNOWN,
                STATE_UNAVAILABLE,
            ):
                return restored_state == STATE_ON
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._hm_entity.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._hm_entity.turn_off()

    async def async_set_on_time(self, on_time: float) -> None:
        """Set the on time of the light."""
        await self._hm_entity.set_on_time_value(on_time=on_time)


class HaHomematicSysvarSwitch(
    HaHomematicGenericSysvarEntity[HmSysvarSwitch], SwitchEntity
):
    """Representation of the HomematicIP hub switch entity."""

    _attr_entity_registry_enabled_default = False

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._hm_hub_entity.value is True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._hm_hub_entity.send_variable(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._hm_hub_entity.send_variable(False)
