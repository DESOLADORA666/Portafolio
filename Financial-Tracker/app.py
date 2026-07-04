"""
Financial Tracker - Aplicación de Finanzas Personales
Version: 2.0.0
"""

import streamlit as st

from src.models import Cartera
from src.services.persistencia import persistencia
from src.utils.logger import logger
from config.settings import Config

# Importar componentes UI
from ui.componentes.formulario import mostrar_formulario
from ui.componentes.filtros import mostrar_filtros
from ui.componentes.importador import mostrar_importador
from ui.paginas.resumen import mostrar_resumen
from ui.paginas.movimientos import mostrar_movimientos
from ui.paginas.analisis import mostrar_analisis

# ========== CONFIGURACIÓN DE LA PÁGINA ==========
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== INICIALIZACIÓN ==========
def inicializar_estado():
    """Inicializa el estado de la sesión."""
    if "cartera" not in st.session_state:
        logger.info("Cargando cartera desde archivo...")
        st.session_state.cartera = persistencia.cargar()
        logger.info(f"Cartera cargada: {len(st.session_state.cartera)} transacciones")

# ========== SIDEBAR ==========
def renderizar_sidebar():
    """Renderiza el contenido del sidebar."""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.title(Config.APP_NAME)
        st.caption(f"Versión {Config.APP_VERSION}")
        
        st.divider()
        
        # Formulario
        mostrar_formulario()
        
        st.divider()
        
        # Importador
        mostrar_importador()
        
        st.divider()
        
        # Estadísticas rápidas
        cartera = st.session_state.cartera
        if cartera:
            st.caption(f"📊 {len(cartera)} transacciones")
            st.caption(f"💰 Balance: ${cartera.balance():,.2f}".replace(",", "."))

# ========== CUERPO PRINCIPAL ==========
def main():
    """Función principal de la aplicación."""
    # Inicializar estado
    inicializar_estado()
    
    # Renderizar sidebar
    renderizar_sidebar()
    
    # Obtener cartera
    cartera = st.session_state.cartera
    
    # Aplicar filtros
    categorias_seleccionadas, fecha_desde, fecha_hasta = mostrar_filtros(cartera)
    
    cartera_filtrada = cartera.filtrar(
        categorias=categorias_seleccionadas,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    # Mostrar páginas en tabs
    tab1, tab2, tab3 = st.tabs(["📊 Resumen", "📋 Movimientos", "📈 Análisis"])
    
    with tab1:
        mostrar_resumen(cartera_filtrada)
    
    with tab2:
        mostrar_movimientos(cartera_filtrada)
    
    with tab3:
        mostrar_analisis(cartera_filtrada)

# ========== EJECUCIÓN ==========
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {e}", exc_info=True)
        st.error("❌ Ha ocurrido un error inesperado. Por favor, revisa los logs.")