import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN

class AirbnbConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Erstellung eines völlig freien AirBnB Modus."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"AirBnB: {user_input['custom_mode_name']}", 
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                # Freier Name für den Modus
                vol.Required("custom_mode_name", default="Check-In"): str,
                vol.Optional("icon", default="mdi:home-heart"): str,
                
                # Auswahl der Geräte
                vol.Required("target_entities"): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain=["light", "switch", "media_player", "notify"], 
                        multiple=True
                    )
                ),
                
                # Konfiguration der Nachricht
                vol.Optional("welcome_message", default="Willkommen in deiner Unterkunft!"): str,
                
                # Konfiguration für Media Player
                vol.Optional("media_volume", default=30): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=100, unit_of_measurement="%", mode="slider")
                ),
                vol.Optional("media_content_id"): str, # Link zur Playlist oder Song
            })
        )