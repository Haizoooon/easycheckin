from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

PLATFORMS = ["scene"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup der AirBnB Suite."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entfernen der Integration."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)