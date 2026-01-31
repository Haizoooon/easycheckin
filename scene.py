from homeassistant.components.scene import Scene
from typing import Any

async def async_setup_entry(hass, entry, async_add_entities):
    """Dies ist der Fix für deinen Log-Fehler!"""
    async_add_entities([AirbnbModeScene(hass, entry)])

class AirbnbModeScene(Scene):
    def __init__(self, hass, entry):
        self.hass = hass
        self._entry = entry
        # Wir nutzen eine Property für Namen und Icon, damit sie sich bei Updates ändern
        self._attr_unique_id = f"airbnb_custom_{entry.entry_id}"

    @property
    def name(self):
        """Holt den Namen dynamisch (wichtig für Umbenennungen)."""
        return self._entry.options.get("custom_mode_name", self._entry.data.get("custom_mode_name"))

    @property
    def icon(self):
        """Holt das Icon dynamisch."""
        return self._entry.options.get("icon", self._entry.data.get("icon"))

    async def async_activate(self, **kwargs: Any) -> None:
        """Führt die Szene aus."""
        # Kombiniert Initialdaten mit späteren Änderungen (Options haben Vorrang)
        configs = {**self._entry.data, **self._entry.options}
        
        entities = configs.get("target_entities", [])
        msg = configs.get("welcome_message")
        vol_level = configs.get("media_volume", 30) / 100

        for entity_id in entities:
            domain = entity_id.split(".")[0]
            
            # Lichtsteuerung
            if domain == "light":
                await self.hass.services.async_call("light", "turn_on", {
                    "entity_id": entity_id,
                    "brightness_pct": 80
                })
            
            # Media Player
            elif domain == "media_player":
                await self.hass.services.async_call("media_player", "volume_set", {
                    "entity_id": entity_id,
                    "volume_level": vol_level
                })
                await self.hass.services.async_call("media_player", "media_play", {"entity_id": entity_id})

            # Benachrichtigung
            elif domain == "notify":
                service_name = entity_id.split(".")[1]
                await self.hass.services.async_call("notify", service_name, {"message": msg})