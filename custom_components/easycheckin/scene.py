from homeassistant.components.scene import Scene
from homeassistant.helpers import script

async def async_setup_entry(hass, entry, async_add_entities):
    """Erstellt automatisch die 3 festen Szenen."""
    async_add_entities([
        EasyCheckInFixedScene(hass, entry, "checkin", "Check-In", "mdi:key"),
        EasyCheckInFixedScene(hass, entry, "checkout", "Check-Out", "mdi:exit-run"),
        EasyCheckInFixedScene(hass, entry, "maintenance", "Reinigung", "mdi:vacuum"),
    ])

class EasyCheckInFixedScene(Scene):
    def __init__(self, hass, entry, action_key, name, icon):
        self.hass = hass
        self._entry = entry
        self._action_key = f"{action_key}_actions"
        self._attr_name = f"EasyCheckIn: {name}"
        self._attr_icon = icon
        self._attr_unique_id = f"easy_{entry.entry_id}_{action_key}"

    async def async_activate(self, **kwargs):
        """Führt die hinterlegten Aktionen aus."""
        actions = self._entry.options.get(self._action_key, [])
        if actions:
            await script.Script(self.hass, actions, self._attr_name, "easycheckin").async_run(context=self._context)