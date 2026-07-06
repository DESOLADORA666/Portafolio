"""
Configuracion centralizada del proyecto.
Contiene todas las variables de configuracion en un solo lugar.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ScraperConfig:
    """Configuracion del scraper de Google Play Store."""

    # Identificador de la app a scraperear
    # Ejemplo: "com.whatsapp", "com.instagram.android"
    app_id: str = "com.whatsapp"

    # Idioma de las reviews (ej: "es", "en", "fr")
    lang: str = "es"

    # Pais (ej: "mx", "us", "es")
    country: str = "mx"

    # Numero maximo de reviews a extraer
    max_reviews: int = 500

    # Segundos de espera entre peticiones para evitar bloqueos
    sleep_seconds: int = 2

    # Intentos maximos en caso de error
    max_retries: int = 3

    # Directorio donde se guardaran los archivos de salida
    output_dir: str = "./output"

    # Bandera para exportar a CSV
    export_csv: bool = True

    # Bandera para exportar a Excel
    export_excel: bool = True


@dataclass
class DashboardConfig:
    """Configuracion del dashboard de Streamlit."""

    # Titulo del dashboard
    title: str = "Play Store Data Analyzer"

    # Icono del dashboard
    icon: str = "📊"

    # Configuracion de la pagina
    page_title: str = "Analisis de Apps"
    page_icon: str = "📱"
    layout: str = "wide"


# Diccionario con las apps mas populares y sus IDs
POPULAR_APPS: Dict[str, str] = {
    "whatsapp": "com.whatsapp",
    "instagram": "com.instagram.android",
    "spotify": "com.spotify.music",
    "netflix": "com.netflix.mediaclient",
    "duolingo": "com.duolingo",
    "tinder": "com.tinder",
    "telegram": "org.telegram.messenger",
    "youtube": "com.google.android.youtube",
    "mercadolibre": "com.mercadolibre",
    "tiktok": "com.zhiliaoapp.musically",
}

# Configuracion por defecto
DEFAULT_CONFIG = ScraperConfig()
DEFAULT_DASHBOARD_CONFIG = DashboardConfig()