import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.models import Cartera
from src.utils.validadores import formatear_moneda

def mostrar_analisis(cartera: Cartera):
    """
    Muestra gráficos interactivos de análisis financiero.
    """
    st.header("📈 Análisis de Gastos")
    
    if not cartera:
        st.info("💡 No hay gastos registrados para analizar")
        return
    
    # Verificar si hay gastos
    if cartera.gastos() == 0:
        st.info("💡 No hay gastos registrados. ¡Comienza a registrar tus gastos!")
        return
    
    # ========== GRÁFICO 1: Distribución por Categoría ==========
    st.subheader("Distribución de Gastos por Categoría")
    
    gastos_cat = cartera.gastos_por_categoria()
    df_cat = pd.DataFrame({
        'Categoría': list(gastos_cat.keys()),
        'Monto': list(gastos_cat.values())
    })
    df_cat = df_cat[df_cat['Monto'] > 0]  # Filtrar categorías sin gastos
    
    if not df_cat.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de torta interactivo
            fig_pie = px.pie(
                df_cat,
                values='Monto',
                names='Categoría',
                title='Distribución de Gastos',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hover_data={'Monto': ':$.2f'}
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Tabla de resumen
            df_cat_sorted = df_cat.sort_values('Monto', ascending=False)
            df_cat_sorted['Monto'] = df_cat_sorted['Monto'].apply(formatear_moneda)
            st.dataframe(df_cat_sorted, use_container_width=True, hide_index=True)
    else:
        st.info("No hay datos para mostrar")
    
    # ========== GRÁFICO 2: Evolución Temporal ==========
    st.divider()
    st.subheader("Evolución de Gastos")
    
    gastos_fecha = cartera.gastos_por_fecha()
    if gastos_fecha:
        df_fecha = pd.DataFrame({
            'Fecha': list(gastos_fecha.keys()),
            'Monto': list(gastos_fecha.values())
        })
        df_fecha = df_fecha.sort_values('Fecha')
        
        # Gráfico de líneas
        fig_line = px.line(
            df_fecha,
            x='Fecha',
            y='Monto',
            title='Gastos Diarios',
            labels={'Monto': 'Monto Gastado ($)', 'Fecha': 'Fecha'},
            markers=True
        )
        fig_line.update_layout(
            hovermode='x unified',
            yaxis_tickprefix='$',
            yaxis_tickformat=',.2f'
        )
        fig_line.update_traces(
            line=dict(color='#ff6b6b', width=2),
            marker=dict(color='#ee5a24', size=6)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # ========== GRÁFICO 3: Gastos por Mes ==========
        st.divider()
        st.subheader("Gastos por Mes")
        
        gastos_mes = cartera.gastos_por_mes()
        if gastos_mes:
            df_mes = pd.DataFrame({
                'Mes': list(gastos_mes.keys()),
                'Monto': list(gastos_mes.values())
            })
            df_mes = df_mes.sort_values('Mes')
            
            # Gráfico de barras
            fig_bar = px.bar(
                df_mes,
                x='Mes',
                y='Monto',
                title='Gastos Mensuales',
                labels={'Monto': 'Monto Gastado ($)', 'Mes': 'Mes'},
                color='Monto',
                color_continuous_scale='Reds'
            )
            fig_bar.update_layout(
                yaxis_tickprefix='$',
                yaxis_tickformat=',.2f',
                xaxis_tickangle=-45
            )
            fig_bar.update_traces(
                texttemplate='$%{y:,.2f}',
                textposition='outside'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # ========== ESTADÍSTICAS ADICIONALES ==========
    st.divider()
    with st.expander("📊 Estadísticas Detalladas"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total de Transacciones",
                len(cartera)
            )
        
        with col2:
            num_gastos = sum(1 for t in cartera if t.es_gasto)
            st.metric(
                "Número de Gastos",
                num_gastos
            )
        
        with col3:
            num_ingresos = sum(1 for t in cartera if t.es_ingreso)
            st.metric(
                "Número de Ingresos",
                num_ingresos
            )
        
        if cartera.gastos() > 0:
            # Gasto máximo
            gasto_max = max(t.monto for t in cartera if t.es_gasto)
            st.metric(
                "Gasto Máximo",
                formatear_moneda(gasto_max)
            )