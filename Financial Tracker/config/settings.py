import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración centralizada del proyecto."""
    
    # Rutas
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DATA_FILE = DATA_DIR / "transacciones.csv"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Crear directorios si no existen
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Categorías predefinidas
    CATEGORIAS = ["Comidas", "Transporte", "Salud", "Ocio", "Hogar", "Otros"]
    
    # UI
    ITEMS_POR_PAGINA = 10
    TEMA = os.getenv("STREAMLIT_THEME", "light")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "app.log"
    
    # App
    APP_NAME = "💰 Financial Tracker"
    APP_VERSION = "2.0.0"
    APP_DESCRIPTION = "Lleva el control de tus gastos e ingresos de manera simple y visual"

# Validación de configuración
if not Config.DATA_FILE.parent.exists():
    Config.DATA_FILE.parent.mkdir(parents=True)