from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([EasyCheckInStatusSensor(entry)])

class EasyCheckInStatusSensor(SensorEntity):
    def __init__(self, entry):
        self._attr_name = "EasyCheckIn Status"
        self._attr_unique_id = f"easy_status_{entry.entry_id}"
        self._attr_native_value = "Bereit"
        self._attr_icon = "mdi:home-circle"

    async def async_added_to_hass(self):
        @callback
        def _state_listener(event):
            eid = event.data.get("entity_id")
            if not eid.startswith("scene.easycheckin_"): return
            
            if "checkin" in eid: 
                self._attr_native_value = "checkin" # Statt "Eingecheckt"
                self._attr_icon = "mdi:home-account"
            elif "checkout" in eid: 
                self._attr_native_value = "checkout" # Statt "Ausgecheckt"
                self._attr_icon = "mdi:home-export"
            elif "maintenance" in eid: 
                self._attr_native_value = "maintenance" # Statt "In Reinigung"
                self._attr_icon = "mdi:vacuum"
            
            self.async_write_ha_state()

        self.async_on_remove(async_track_state_change_event(self.hass, ["scene"], _state_listener))