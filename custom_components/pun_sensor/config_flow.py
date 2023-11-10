from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from .const import (
    DOMAIN,
    CONF_SCAN_HOUR,
    CONF_ACTUAL_DATA_ONLY, CONF_FIXED_SERVICE, CONF_VAR_FEE, CONF_VAR_DISP, CONF_VAR_LOST, CONF_VAR_DISPEN,
    CONF_VAR_MAXUC, CONF_VAR_ONERI_ASOS, CONF_VAR_ONERI_ARIM, CONF_TAXES, CONF_IVA,

)

class PUNOptionsFlow(config_entries.OptionsFlow):
    """Opzioni per prezzi PUN (= riconfigurazione successiva)"""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        """Inizializzazione options flow"""
        self.config_entry = entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Gestisce le opzioni"""
        errors = {}
        if user_input is not None:
            # Configurazione valida (validazione integrata nello schema)
            return self.async_create_entry(
                title='PUN',
                data=user_input
            )

        # Schema dati di opzione (con default sui valori attuali)
        data_schema = {
            vol.Required(CONF_SCAN_HOUR, default=self.config_entry.options.get(CONF_SCAN_HOUR, self.config_entry.data[CONF_SCAN_HOUR])): vol.All(cv.positive_int, vol.Range(min=0, max=23)),
            vol.Optional(CONF_ACTUAL_DATA_ONLY, default=self.config_entry.options.get(CONF_ACTUAL_DATA_ONLY, self.config_entry.data[CONF_ACTUAL_DATA_ONLY])): cv.boolean,
        }

        if self.show_advanced_options:
            data_schema[vol.Optional(CONF_FIXED_SERVICE, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_FEE, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_DISP, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_LOST, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_DISPEN, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_MAXUC, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_ONERI_ASOS, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_ONERI_ARIM, default=0)]: float
            data_schema[vol.Optional(CONF_TAXES, default=0)]: float
            data_schema[vol.Optional(CONF_IVA, default=10)]: vol.All(cv.positive_int, vol.Range(min=0, max=100))

        # Mostra la schermata di configurazione, con gli eventuali errori
        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(data_schema), errors=errors
        )
    
class PUNConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configurazione per prezzi PUN (= prima configurazione)"""

    # Versione della configurazione (per utilizzi futuri)
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(entry: config_entries.ConfigEntry) -> PUNOptionsFlow:
        """Ottiene le opzioni per questa configurazione"""
        return PUNOptionsFlow(entry)

    async def async_step_user(self, user_input=None):
        """Gestione prima configurazione da Home Assistant"""
        # Controlla che l'integrazione non venga eseguita più volte
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors = {}
        if user_input is not None:
            # Configurazione valida (validazione integrata nello schema)
            return self.async_create_entry(
                title='PUN',
                data=user_input
            )

        # Schema dati di configurazione (con default fissi)
        data_schema = {
            vol.Required(CONF_SCAN_HOUR, default=1): vol.All(cv.positive_int, vol.Range(min=0, max=23)),
            vol.Optional(CONF_ACTUAL_DATA_ONLY, default=False): cv.boolean,

        }


        if self.show_advanced_options:
            data_schema[vol.Optional(CONF_FIXED_SERVICE, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_FEE, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_DISP, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_LOST, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_DISPEN, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_MAXUC, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_ONERI_ASOS, default=0)]: float
            data_schema[vol.Optional(CONF_VAR_ONERI_ARIM, default=0)]: float
            data_schema[vol.Optional(CONF_TAXES, default=0)]: float
            data_schema[vol.Optional(CONF_IVA, default=10)]:  vol.All(cv.positive_int, vol.Range(min=0, max=100))


        # Mostra la schermata di configurazione, con gli eventuali errori
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )

