import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import DOMAIN

class EasyCheckInConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for easycheckin."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initialer Setup-Schritt."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            return self.async_create_entry(title="easycheckin Suite", data=user_input)

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Gibt den Options Flow zurück."""
        return EasyCheckInOptionsFlowHandler(config_entry)

class EasyCheckInOptionsFlowHandler(config_entries.OptionsFlow):
    """Verwaltet die Optionen (Aktionen) im Nachhinein."""
    
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialisieren der Optionen."""
        # Hier lag der Fehler: Wir nennen die Variable um in _config_entry
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Verwalte die Aktionen."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Aktuelle Optionen laden
        curr = self._config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("checkin_actions", default=curr.get("checkin_actions", [])): selector.ActionSelector(),
                vol.Required("checkout_actions", default=curr.get("checkout_actions", [])): selector.ActionSelector(),
                vol.Required("maintenance_actions", default=curr.get("maintenance_actions", [])): selector.ActionSelector(),
            })
        )