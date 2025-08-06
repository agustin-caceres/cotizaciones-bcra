import argparse
import logging
from .client import BcraClient
from .repository import get_latest_date, insert_cotizaciones
from .utils import normalizar_datos

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def carga_inicial():
    client = BcraClient()
    data = client.obtener_cotizaciones()
    normalizados = normalizar_datos(data)
    insert_cotizaciones(normalizados)
    logging.info(f"✅ Carga inicial completa: {len(normalizados)} registros procesados.")

def carga_incremental():
    client = BcraClient()
    data = client.obtener_cotizaciones()
    normalizados = normalizar_datos(data)
    ultima_fecha = get_latest_date()

    nuevos = [item for item in normalizados if ultima_fecha is None or item["fecha"] > ultima_fecha]
    if nuevos:
        insert_cotizaciones(nuevos)
        logging.info(f"✅ Carga incremental completa: {len(nuevos)} registros insertados.")
    else:
        logging.info("ℹ️ No hay nuevas cotizaciones para insertar.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingesta de cotizaciones BCRA")
    parser.add_argument("--modo", choices=["inicial", "incremental"], required=True)
    args = parser.parse_args()

    if args.modo == "inicial":
        carga_inicial()
    elif args.modo == "incremental":
        carga_incremental()
