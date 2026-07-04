import streamlit as st
from datetime import date

from src.models import Transaccion
from src.services.persistencia import persistencia
from src.utils.logger import logger
from config.settings import Config

def mostrar_formulario() -> bool:
    """
    Muestra el formulario para agregar transacciones.
    Retorna True si se agregó una transacción exitosamente.
    """
    with st.form("nueva_transaccion", clear_on_submit=True):
        st.markdown("### 📝 Nueva Transacción")
        
        col1, col2 = st.columns(2)
        
        with col1:
            descripcion = st.text_input(
                "Descripción",
                placeholder="Ej: Compra supermercado",
                help="Describe brevemente la transacción"
            )
            
            monto = st.number_input(
                "Monto ($)",
                min_value=0.01,
                step=0.01,
                format="%0.2f",
                help="Ingresa el monto en dólares"
            )
        
        with col2:
            fecha = st.date_input(
                "Fecha",
                value=date.today(),
                max_value=date.today()
            )
            
            categoria = st.selectbox(
                "Categoría",
                options=Config.CATEGORIAS,
                help="Selecciona la categoría de la transacción"
            )
        
        tipo = st.radio(
            "Tipo",
            options=["Ingreso", "Gasto"],
            horizontal=True,
            help="¿Es un ingreso o un gasto?"
        )
        
        enviado = st.form_submit_button(
            "Agregar Transacción",
            use_container_width=True,
            type="primary"
        )
    
    if enviado:
        # Validaciones
        if not descripcion or not descripcion.strip():
            st.error("❌ La descripción es obligatoria")
            return False
        
        if monto <= 0:
            st.error("❌ El monto debe ser mayor a cero")
            return False
        
        try:
            # Crear transacción
            transaccion = Transaccion(
                descripcion=descripcion.strip(),
                monto=monto,
                fecha=fecha,
                categoria=categoria,
                tipo=tipo
            )
            
            # Agregar a la cartera
            st.session_state.cartera.agregar(transaccion)
            
            # Guardar en archivo
            if persistencia.guardar(st.session_state.cartera):
                st.success("✅ Transacción agregada exitosamente!")
                logger.info(f"Transacción agregada: {transaccion}")
                return True
            else:
                st.error("❌ Error al guardar la transacción")
                return False
                
        except ValueError as e:
            st.error(f"❌ Error de validación: {e}")
            logger.warning(f"Error de validación en formulario: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Error inesperado: {e}")
            logger.error(f"Error en formulario: {e}", exc_info=True)
            return False
    
    return False