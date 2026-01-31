from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

PLATFORMS = ["scene"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup der AirBnB Suite."""
    
    # Dieser Listener beobachtet, ob du auf "Konfigurieren" klickst und speicherst
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Wird aufgerufen, wenn die Optionen aktualisiert werden."""
    # Veranlasst Home Assistant, die Integration mit den neuen Werten neu zu starten
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entfernen der Integration."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)