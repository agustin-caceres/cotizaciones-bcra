# Documentación Técnica — Ejercicio 2: Ingesta de Cotizaciones del BCRA

## 1. Cómo fue construida la ingesta incremental

* **Fuente de datos**: API pública del BCRA, endpoint `https://api.estadisticasbcra.com/usd_of`.
* **Autenticación**: token personal suministrado por el BCRA (`BCRA_API_TOKEN`) enviado en el header `Authorization: BEARER <token>`.
* **Frecuencia de ejecución**: semanal, automatizada con GitHub Actions (lunes 03:00 UTC) y disparo manual vía `workflow_dispatch`.
* **Mecanismo incremental**:

  1. La API devuelve TODO el histórico completo en cada request.
  2. El script consulta `SELECT MAX(fecha) FROM cotizaciones` para conocer la última fecha almacenada.
  3. Filtra en memoria los registros cuya `fecha` sea **mayor** que ese valor.
  4. Inserta los nuevos registros con `INSERT … ON CONFLICT (fecha) DO NOTHING`, evitando duplicados.
* **Idempotencia y robustez**: si una corrida falla o se omite, la siguiente recupera automáticamente las fechas pendientes.

## 2. Ejemplo de ejecución inicial

```bash
python -m cotizaciones_bcra.main --modo inicial
```

Salida típica:

```
Solicitando cotizaciones al BCRA...
3 470 registros recibidos de la API del BCRA.
3 470 registros insertados.
```

## 3. Ejemplo de ejecución incremental

```bash
python -m cotizaciones_bcra.main --modo incremental
```

Salida típica:

```
Solicitando cotizaciones al BCRA...
3 471 registros recibidos de la API del BCRA.
Última fecha registrada: 2025‑08‑06
1 nuevos registros insertados.
```

Si no hay datos nuevos:

```
No hay nuevas cotizaciones para insertar.
```

## 4. Acceso a la base PostgreSQL en la nube

* **Proveedor**: Neon (PostgreSQL Cloud).
* **Cadena de conexión**: gestionada a través de la variable de entorno/secret `DATABASE_URL` con la forma:

  ```
  postgresql+psycopg2://usuario:contraseña@host:puerto/basededatos
  ```
* Las credenciales se almacenan como **Secrets** (`DATABASE_URL`, `BCRA_API_TOKEN`) en el repositorio de GitHub y no se publican por motivos de seguridad.

---

Con esto se cumple la consigna del Ejercicio 2: carga histórica, ingesta incremental semanal y documentación completa.