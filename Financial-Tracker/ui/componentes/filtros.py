import streamlit as st
from datetime import date
from typing import Tuple, List, Optional

from src.models import Cartera
from config.settings import Config

def mostrar_filtros(cartera: Cartera) -> Tuple[List[str], date, date]:
    """
    Muestra los filtros en el sidebar.
    Retorna (categorias_seleccionadas, fecha_desde, fecha_hasta)
    """
    with st.sidebar:
        st.markdown("### 🔍 Filtros")
        
        # Filtro de categorías
        categorias_seleccionadas = st.multiselect(
            "Categorías",
            options=Config.CATEGORIAS,
            default=Config.CATEGORIAS,
            help="Selecciona las categorías que quieres ver"
        )
        
        # Determinar fechas por defecto
        if len(cartera) > 0:
            fechas = [t.fecha for t in cartera.transacciones]
            fecha_desde_default = min(fechas)
            fecha_hasta_default = max(fechas)
        else:
            fecha_desde_default = date.today().replace(day=1)
            fecha_hasta_default = date.today()
        
        # Filtro de fechas
        col1, col2 = st.columns(2)
        with col1:
            fecha_desde = st.date_input(
                "Desde",
                value=fecha_desde_default,
                max_value=date.today()
            )
        with col2:
            fecha_hasta = st.date_input(
                "Hasta",
                value=fecha_hasta_default,
                max_value=date.today()
            )
        
        # Validar fechas
        if fecha_desde > fecha_hasta:
            st.warning("⚠️ La fecha 'Desde' no puede ser mayor que 'Hasta'")
        
        # Mostrar resumen de filtros
        st.caption(f"Mostrando {len(cartera)} transacciones")
        
        return categorias_seleccionadas, fecha_desde, fecha_hasta