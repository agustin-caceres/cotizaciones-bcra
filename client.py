import requests
import logging
from typing import List, Dict
from config import BCRA_API_TOKEN

logger = logging.getLogger(__name__)

API_URL = "https://api.estadisticasbcra.com/usd_of"

class BcraClient:
    """
    Cliente para consultar la API del BCRA y obtener las cotizaciones oficiales del dólar tipo vendedor.
    """
    def __init__(self, token: str = BCRA_API_TOKEN):
        self.headers = {
            "Authorization": f"BEARER {token}"
        }

    def obtener_cotizaciones(self) -> List[Dict]:
        """
        Realiza la consulta a la API y devuelve la respuesta como lista de diccionarios.
        """
        logger.info("Solicitando cotizaciones al BCRA...")
        response = requests.get(API_URL, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"✅ {len(data)} registros recibidos de la API del BCRA.")
        return data
