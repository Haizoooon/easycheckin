from homeassistant.components.scene import Scene
from typing import Any

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([AirbnbModeScene(hass, entry)])

class AirbnbModeScene(Scene):
    def __init__(self, hass, entry):
        self.hass = hass
        self._entry = entry
        # Wir ziehen die Daten aus dem Entry (und den Optionen falls geändert)
        self._data = {**entry.data, **entry.options}
        
        self._attr_name = self._data.get("custom_mode_name")
        self._attr_icon = self._data.get("icon")
        self._attr_unique_id = f"airbnb_custom_{entry.entry_id}"

    async def async_activate(self, **kwargs: Any) -> None:
        """Führt genau das aus, was im Modus konfiguriert wurde."""
        configs = {**self._entry.data, **self._entry.options}
        entities = configs.get("target_entities", [])
        msg = configs.get("welcome_message")
        vol_level = configs.get("media_volume", 30) / 100
        media_url = configs.get("media_content_id")

        for entity_id in entities:
            domain = entity_id.split(".")[0]

            # 1. Lichter & Schalter
            if domain in ["light", "switch"]:
                await self.hass.services.async_call(domain, "turn_on", {"entity_id": entity_id})

            # 2. Media Player (mit Lautstärke und Playlist)
            elif domain == "media_player":
                await self.hass.services.async_call("media_player", "volume_set", {
                    "entity_id": entity_id, 
                    "volume_level": vol_level
                })
                if media_url:
                    await self.hass.services.async_call("media_player", "play_media", {
                        "entity_id": entity_id,
                        "media_content_id": media_url,
                        "media_content_type": "music"
                    })
                else:
                    await self.hass.services.async_call("media_player", "media_play", {"entity_id": entity_id})

            # 3. Benachrichtigungen
            elif domain == "notify" or domain == "persistent_notification":
                service = "create" if domain == "persistent_notification" else entity_id.split(".")[1]
                await self.hass.services.async_call(domain, service, {
                    "title": "AirBnB Update",
                    "message": msg
                })