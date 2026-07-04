import streamlit as st
import pandas as pd
from datetime import datetime

from src.models import Cartera
from src.utils.validadores import formatear_moneda

def mostrar_resumen(cartera: Cartera):
    """
    Muestra el dashboard con métricas clave.
    """
    st.header("📊 Resumen Financiero")
    
    if not cartera:
        st.info("💡 No hay transacciones para mostrar. ¡Agrega tu primera transacción!")
        return
    
    # Métricas principales
    ingresos = cartera.ingresos()
    gastos = cartera.gastos()
    balance = cartera.balance()
    gasto_promedio = cartera.gasto_promedio()
    
    # Determinar color del balance
    if balance > 0:
        delta_color = "normal"
        delta_text = "⬆️ Positivo"
    elif balance < 0:
        delta_color = "inverse"
        delta_text = "⬇️ Negativo"
    else:
        delta_color = "off"
        delta_text = "⚖️ Equilibrado"
    
    # Columnas de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Ingresos",
            value=formatear_moneda(ingresos),
            delta=f"+{formatear_moneda(ingresos - gastos)}" if ingresos > gastos else None
        )
    
    with col2:
        st.metric(
            label="💳 Gastos",
            value=formatear_moneda(gastos)
        )
    
    with col3:
        st.metric(
            label="📈 Balance",
            value=formatear_moneda(balance),
            delta=delta_text,
            delta_color=delta_color
        )
    
    with col4:
        st.metric(
            label="📊 Gasto Promedio",
            value=formatear_moneda(gasto_promedio)
        )
    
    # Transacciones recientes
    st.divider()
    st.subheader("🕐 Transacciones Recientes")
    
    recientes = cartera.transacciones_recientes(n=5)
    if recientes:
        df = pd.DataFrame([t.to_dict() for t in recientes])
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%d/%m/%Y')
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay transacciones recientes")