import pandas as pd
from pathlib import Path
from typing import Optional
from datetime import date

from src.models import Transaccion, Cartera
from src.utils.logger import logger
from src.utils.validadores import validar_fecha
from config.settings import Config

class Persistencia:
    """
    Maneja la persistencia de datos en CSV.
    """
    
    @staticmethod
    def guardar(cartera: Cartera, archivo: Optional[Path] = None) -> bool:
        """
        Guarda la cartera en un archivo CSV.
        Retorna True si fue exitoso.
        """
        if archivo is None:
            archivo = Config.DATA_FILE
        
        try:
            df = cartera.to_dataframe()
            if df.empty:
                logger.warning("Intentando guardar cartera vacía")
                # Guardar solo el header
                df = pd.DataFrame(columns=['descripcion', 'monto', 'fecha', 'categoria', 'tipo'])
            
            df.to_csv(archivo, index=False, encoding='utf-8')
            logger.info(f"Cartera guardada exitosamente en {archivo} ({len(cartera)} transacciones)")
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar cartera: {e}")
            return False
    
    @staticmethod
    def cargar(archivo: Optional[Path] = None) -> Cartera:
        """
        Carga una cartera desde un archivo CSV.
        Si el archivo no existe o es inválido, retorna una cartera vacía.
        """
        if archivo is None:
            archivo = Config.DATA_FILE
        
        if not archivo.exists():
            logger.info(f"Archivo {archivo} no encontrado, creando cartera nueva")
            return Cartera()
        
        try:
            df = pd.read_csv(archivo, encoding='utf-8')
            
            # Validar columnas
            columnas_esperadas = {'descripcion', 'monto', 'fecha', 'categoria', 'tipo'}
            columnas_faltantes = columnas_esperadas - set(df.columns)
            
            if columnas_faltantes:
                logger.error(f"Columnas faltantes en CSV: {columnas_faltantes}")
                return Cartera()
            
            # Convertir filas a Transacciones
            transacciones = []
            for idx, row in df.iterrows():
                try:
                    # Validar fecha
                    if not validar_fecha(row['fecha']):
                        logger.warning(f"Fecha inválida en fila {idx}: {row['fecha']}")
                        continue
                    
                    transaccion = Transaccion.from_dict(row.to_dict())
                    transacciones.append(transaccion)
                    
                except Exception as e:
                    logger.warning(f"Error al procesar fila {idx}: {e}")
                    continue
            
            cartera = Cartera(transacciones)
            logger.info(f"Cartera cargada exitosamente: {len(cartera)} transacciones")
            return cartera
            
        except pd.errors.EmptyDataError:
            logger.warning(f"Archivo {archivo} está vacío")
            return Cartera()
            
        except Exception as e:
            logger.error(f"Error al cargar cartera: {e}")
            return Cartera()

# Singleton para facilitar el uso
persistencia = Persistencia()