import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import Optional

from src.models import Cartera
from src.utils.logger import logger

class Exportador:
    """
    Exporta datos en diferentes formatos.
    """
    
    @staticmethod
    def a_excel(cartera: Cartera, incluir_resumen: bool = True) -> BytesIO:
        """
        Exporta la cartera a Excel con formato profesional.
        Retorna un objeto BytesIO para descarga.
        """
        output = BytesIO()
        
        try:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Hoja de transacciones
                df = cartera.to_dataframe()
                if not df.empty:
                    df.to_excel(writer, sheet_name='Transacciones', index=False)
                    
                    # Formato automático
                    workbook = writer.book
                    worksheet = writer.sheets['Transacciones']
                    
                    # Ajustar ancho de columnas
                    for i, col in enumerate(df.columns):
                        max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                        worksheet.set_column(i, i, min(max_len, 30))
                
                # Hoja de resumen
                if incluir_resumen:
                    resumen = pd.DataFrame({
                        'Métrica': ['Ingresos', 'Gastos', 'Balance', 'Gasto Promedio', 
                                   'Total Transacciones'],
                        'Valor': [
                            cartera.ingresos(),
                            cartera.gastos(),
                            cartera.balance(),
                            cartera.gasto_promedio(),
                            len(cartera)
                        ]
                    })
                    resumen.to_excel(writer, sheet_name='Resumen', index=False)
                
                # Metadatos
                workbook = writer.book
                doc_properties = {
                    'title': 'Reporte Financiero',
                    'subject': 'Finanzas Personales',
                    'author': 'Financial Tracker',
                    'company': 'Portfolio Project',
                    'created': datetime.now()
                }
                workbook.set_properties(doc_properties)
                
            output.seek(0)
            logger.info(f"Excel exportado exitosamente ({len(cartera)} transacciones)")
            return output
            
        except Exception as e:
            logger.error(f"Error al exportar a Excel: {e}")
            raise
    
    @staticmethod
    def a_csv(cartera: Cartera) -> str:
        """
        Exporta la cartera a formato CSV (string).
        """
        df = cartera.to_dataframe()
        if df.empty:
            return ""
        return df.to_csv(index=False, encoding='utf-8')

# Singleton
exportador = Exportador()