"""
Play Store Scraper - Punto de entrada principal.

Ejecuta el scraper para una app especifica y exporta los datos.
"""

import logging

from config.settings import DEFAULT_CONFIG, POPULAR_APPS
from src.scraper import PlayStoreScraper
from src.exporter import Exporter

# Configurar logging para seguimiento de ejecucion
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# ============================================================
# CONFIGURACION - CAMBIAR AQUI LA APP A SCRAPEREAR
# ============================================================

# Opcion 1: Usar un app_id directamente
APP_ID = "com.duolingo"

# Opcion 2: Usar un nombre de app popular (descomentar)
# APP_ID = POPULAR_APPS["instagram"]

# Opcion 3: Cambiar la configuracion completa
# config = DEFAULT_CONFIG
# config.app_id = "com.spotify.music"
# config.lang = "en"
# config.country = "us"
# config.max_reviews = 1000

# ============================================================


def main() -> None:
    """Funcion principal del scraper."""
    print("\n" + "=" * 60)
    print("PLAY STORE SCRAPER")
    print("Extrayendo datos de Google Play Store")
    print("=" * 60 + "\n")

    # Crear scraper con la configuracion por defecto
    scraper = PlayStoreScraper(DEFAULT_CONFIG)

    # Cambiar el app_id a la app deseada
    scraper.config.app_id = APP_ID

    # Ejecutar scraper
    result = scraper.run()

    if not result["app_info"]:
        print("No se pudo obtener informacion de la app")
        return

    # Exportar datos
    exporter = Exporter(scraper)
    exporter.export_all(output_dir="./output")

    print("\nProceso completado exitosamente")


if __name__ == "__main__":
    main()