from datetime import datetime
from typing import List, Dict

def normalizar_datos(data: List[Dict]) -> List[Dict]:
    """
    Convierte los datos crudos de la API del BCRA en registros compatibles con la tabla cotizaciones.

    Parámetros:
        data (List[Dict]): Lista de registros con claves 'd' (fecha) y 'v' (valor).

    Devuelve:
        List[Dict]: Lista de diccionarios normalizados con claves 'fecha', 'moneda', 'tipo_cambio', 'fuente'.
    """
    return [
        {
            "fecha": datetime.strptime(item["d"], "%Y-%m-%d").date(),
            "moneda": "Dólar",
            "tipo_cambio": round(float(item["v"]), 4),
            "fuente": "BCRA"
        }
        for item in data
    ]
