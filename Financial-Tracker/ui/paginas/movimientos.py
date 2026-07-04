import streamlit as st
import pandas as pd

from src.models import Cartera
from src.services.exportador import exportador
from config.settings import Config

def mostrar_movimientos(cartera: Cartera):
    """
    Muestra la tabla de transacciones con paginación y opciones de exportación.
    """
    st.header("📋 Movimientos")
    
    if not cartera:
        st.info("💡 No hay transacciones para mostrar")
        return
    
    df = cartera.to_dataframe()
    
    # Formatear fechas para visualización
    df_visual = df.copy()
    df_visual['fecha'] = pd.to_datetime(df_visual['fecha']).dt.strftime('%d/%m/%Y')
    df_visual['monto'] = df_visual['monto'].apply(lambda x: f"${x:,.2f}".replace(",", "."))
    
    # Paginación
    total_items = len(df_visual)
    items_por_pagina = Config.ITEMS_POR_PAGINA
    
    if total_items > items_por_pagina:
        total_paginas = (total_items - 1) // items_por_pagina + 1
        
        col1, col2 = st.columns([1, 3])
        with col1:
            pagina = st.selectbox(
                "Página",
                range(1, total_paginas + 1),
                index=0,
                label_visibility="collapsed"
            )
        
        inicio = (pagina - 1) * items_por_pagina
        fin = min(inicio + items_por_pagina, total_items)
        df_visual = df_visual.iloc[inicio:fin]
        
        st.caption(f"Mostrando {inicio + 1} - {fin} de {total_items} transacciones")
    
    # Mostrar tabla
    st.dataframe(
        df_visual,
        use_container_width=True,
        column_config={
            "descripcion": "Descripción",
            "monto": st.column_config.TextColumn("Monto"),
            "fecha": "Fecha",
            "categoria": "Categoría",
            "tipo": st.column_config.TextColumn("Tipo", width="small")
        }
    )
    
    # Botones de exportación
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Exportar CSV
        csv_data = exportador.a_csv(cartera)
        if csv_data:
            st.download_button(
                label="📄 Descargar CSV",
                data=csv_data,
                file_name="transacciones.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        # Exportar Excel
        try:
            excel_data = exportador.a_excel(cartera)
            st.download_button(
                label="📊 Descargar Excel",
                data=excel_data,
                file_name="transacciones.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.warning("⚠️ No se pudo generar Excel")