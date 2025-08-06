import logging
from sqlalchemy import create_engine, text
from .config import DATABASE_URL

logger = logging.getLogger(__name__)

# ─────────────────────────── Engine ────────────────────────────
engine = create_engine(DATABASE_URL, future=True)

# ─────────────────────── Consultas auxiliares ──────────────────
def get_latest_date():
    """
    Devuelve la fecha máxima registrada en la tabla cotizaciones.
    Si la tabla está vacía, devuelve None.
    """
    query = text("SELECT MAX(fecha) FROM cotizaciones")
    with engine.connect() as conn:
        result = conn.execute(query).scalar()
    logger.info(f"📅 Última fecha registrada: {result}")
    return result


# ───────────────────────── Inserción bulk ──────────────────────
def insert_cotizaciones(data, batch_size: int = 500):
    """
    Inserta los registros recibidos en lotes para mejorar la performance.
    Muestra logs de avance cada `batch_size` filas.

    Args:
        data (list[dict]): Registros normalizados listos para insertar.
        batch_size (int): Tamaño del lote para la inserción por partes.
    """
    if not data:
        logger.info("ℹ️ No hay datos para insertar.")
        return

    query = text("""
        INSERT INTO cotizaciones (fecha, moneda, tipo_cambio, fuente)
        VALUES (:fecha, :moneda, :tipo_cambio, :fuente)
        ON CONFLICT (fecha) DO NOTHING
    """)

    total = len(data)
    with engine.begin() as conn:
        for i in range(0, total, batch_size):
            batch = data[i:i + batch_size]
            conn.execute(query, batch)          # executemany automático
            logger.info(f"📦 Insertados {i + len(batch):>5} / {total} registros...")

    logger.info(f"✅ Inserción completa: {total} registros procesados.")