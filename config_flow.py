import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN

class EasyCheckInConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initiales Setup."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            return self.async_create_entry(title="EasyCheckIn Suite", data=user_input)

        return self.async_show_form(step_id="user")

    @staticmethod
    def async_get_options_flow(config_entry):
        return EasyCheckInOptionsFlowHandler(config_entry)

class EasyCheckInOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Hier werden die Aktionen für die festen Szenen verwaltet."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        curr = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("checkin_actions", default=curr.get("checkin_actions", [])): selector.ActionSelector(),
                vol.Required("checkout_actions", default=curr.get("checkout_actions", [])): selector.ActionSelector(),
                vol.Required("maintenance_actions", default=curr.get("maintenance_actions", [])): selector.ActionSelector(),
            })
        )