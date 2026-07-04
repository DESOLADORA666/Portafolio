import streamlit as st
import pandas as pd
from datetime import date

from src.models import Transaccion
from src.services.persistencia import persistencia
from src.utils.logger import logger
from config.settings import Config

def mostrar_importador():
    """
    Permite importar transacciones desde un archivo CSV.
    """
    with st.sidebar.expander("📥 Importar desde CSV"):
        st.markdown("Importa transacciones desde un archivo CSV")
        st.caption("El CSV debe tener: descripcion, monto, fecha, categoria, tipo")
        
        archivo_subido = st.file_uploader(
            "Selecciona un archivo CSV",
            type=["csv"],
            help="Formato esperado: descripcion,monto,fecha(YYYY-MM-DD),categoria,tipo"
        )
        
        if archivo_subido:
            # Previsualizar
            try:
                df_preview = pd.read_csv(archivo_subido, nrows=5)
                st.dataframe(df_preview, use_container_width=True)
            except Exception:
                st.error("❌ El archivo no es un CSV válido")
                return
            
            col1, col2 = st.columns(2)
            with col1:
                boton_importar = st.button("📤 Importar", use_container_width=True, type="primary")
            with col2:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.rerun()
            
            if boton_importar:
                try:
                    # Leer todo el archivo
                    archivo_subido.seek(0)  # Resetear puntero
                    df = pd.read_csv(archivo_subido)
                    
                    # Validar columnas
                    columnas_esperadas = {'descripcion', 'monto', 'fecha', 'categoria', 'tipo'}
                    columnas_faltantes = columnas_esperadas - set(df.columns)
                    
                    if columnas_faltantes:
                        st.error(f"❌ Columnas faltantes: {', '.join(columnas_faltantes)}")
                        return
                    
                    # Convertir a transacciones
                    nuevas_transacciones = []
                    errores = 0
                    
                    for idx, row in df.iterrows():
                        try:
                            transaccion = Transaccion(
                                descripcion=str(row["descripcion"]),
                                monto=float(row["monto"]),
                                fecha=date.fromisoformat(str(row["fecha"])),
                                categoria=str(row["categoria"]),
                                tipo=str(row["tipo"])
                            )
                            nuevas_transacciones.append(transaccion)
                        except Exception as e:
                            errores += 1
                            logger.warning(f"Error en fila {idx}: {e}")
                            continue
                    
                    if not nuevas_transacciones:
                        st.error("❌ No se pudo importar ninguna transacción")
                        return
                    
                    # Agregar a la cartera
                    for t in nuevas_transacciones:
                        st.session_state.cartera.agregar(t)
                    
                    # Guardar
                    if persistencia.guardar(st.session_state.cartera):
                        st.success(f"✅ Se importaron {len(nuevas_transacciones)} transacciones")
                        if errores > 0:
                            st.warning(f"⚠️ {errores} filas fueron omitidas por errores")
                        logger.info(f"Importadas {len(nuevas_transacciones)} transacciones")
                    else:
                        st.error("❌ Error al guardar las transacciones importadas")
                        
                except Exception as e:
                    st.error(f"❌ Error al importar: {e}")
                    logger.error(f"Error en importación: {e}", exc_info=True)