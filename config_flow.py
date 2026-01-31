import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import DOMAIN

class AirbnbConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Aktiviert das Bearbeitungs-Menü."""
        return AirbnbOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Ersterstellung eines Modus."""
        if user_input is not None:
            return self.async_create_entry(title=f"AirBnB: {user_input['custom_mode_name']}", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema()
        )

    def _get_schema(self, defaults=None):
        """Hilfsfunktion für das Formular-Layout."""
        if defaults is None:
            defaults = {}
        return vol.Schema({
            vol.Required("custom_mode_name", default=defaults.get("custom_mode_name", "Check-In")): str,
            vol.Optional("icon", default=defaults.get("icon", "mdi:home-heart")): str,
            vol.Required("target_entities", default=defaults.get("target_entities", [])): selector.EntitySelector(
                selector.EntitySelectorConfig(domain=["light", "switch", "media_player", "notify"], multiple=True)
            ),
            vol.Optional("welcome_message", default=defaults.get("welcome_message", "Willkommen!")): str,
            vol.Optional("media_volume", default=defaults.get("media_volume", 30)): selector.NumberSelector(
                selector.NumberSelectorConfig(min=0, max=100, mode="slider")
            ),
        })

class AirbnbOptionsFlowHandler(config_entries.OptionsFlow):
    """Hier passiert die Bearbeitung im Nachhinein."""
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # Speichert die Änderungen in entry.options
            return self.async_create_entry(title="", data=user_input)

        # Aktuelle Werte laden, damit sie im Formular vorausgefüllt sind
        current_data = {**self.config_entry.data, **self.config_entry.options}
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("icon", default=current_data.get("icon")): str,
                vol.Required("target_entities", default=current_data.get("target_entities")): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["light", "switch", "media_player", "notify"], multiple=True)
                ),
                vol.Optional("welcome_message", default=current_data.get("welcome_message")): str,
                vol.Optional("media_volume", default=current_data.get("media_volume")): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=100, mode="slider")
                ),
            })
        )