"""
Modulo exporter - Exporta datos a CSV y Excel.

Convierte los datos extraidos a diferentes formatos para
su posterior analisis o visualizacion.
"""

import os
from typing import Dict, List, Optional, Tuple

import pandas as pd
from openpyxl.utils import get_column_letter

from config.settings import ScraperConfig
from src.scraper import PlayStoreScraper


class Exporter:
    """
    Exporta los datos del scraper a archivos CSV y Excel.

    Mantiene el formato de los datos y ajusta automaticamente
    el ancho de las columnas para una mejor visualizacion.

    Attributes:
        scraper: Instancia de PlayStoreScraper con los datos
        app_info: Informacion de la app
        reviews: Lista de reviews
        timestamp: Marca de tiempo de la ejecucion
        app_id_clean: ID de la app limpio para nombres de archivo
        config: Configuracion del scraper
    """

    def __init__(self, scraper: PlayStoreScraper):
        """
        Inicializa el exporter con los datos del scraper.

        Args:
            scraper: Instancia de PlayStoreScraper con datos extraidos
        """
        self.scraper = scraper
        self.app_info = scraper.app_info
        self.reviews = scraper.reviews_data
        self.timestamp = scraper.timestamp
        self.app_id_clean = scraper.config.app_id.replace(".", "_")
        self.config = scraper.config

    def _ensure_output_dir(self, output_dir: str) -> None:
        """
        Crea el directorio de salida si no existe.

        Args:
            output_dir: Ruta del directorio a crear
        """
        os.makedirs(output_dir, exist_ok=True)

    def _get_base_filename(self) -> str:
        """
        Genera el nombre base para los archivos de salida.

        El formato es: app_id_timestamp

        Returns:
            Nombre base del archivo.
        """
        return f"{self.app_id_clean}_{self.timestamp}"

    def to_dataframe(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Convierte los datos a DataFrames de pandas.

        Returns:
            Tupla con (info_df, reviews_df)
        """
        # DataFrame de informacion de la app
        info_df = pd.DataFrame([self.app_info]) if self.app_info else pd.DataFrame()

        # DataFrame de reviews
        reviews_df = pd.DataFrame(self.reviews) if self.reviews else pd.DataFrame()

        return info_df, reviews_df

    def to_csv(self, output_dir: Optional[str] = None) -> Optional[str]:
        """
        Exporta los datos a archivos CSV.

        Genera dos archivos: uno con la informacion de la app
        y otro con las reviews.

        Args:
            output_dir: Directorio de salida (usa el de config si no se especifica)

        Returns:
            Ruta del archivo CSV de reviews, o None si falla.
        """
        output_dir = output_dir or self.config.output_dir
        self._ensure_output_dir(output_dir)

        info_df, reviews_df = self.to_dataframe()

        if reviews_df.empty:
            print("No hay datos para exportar a CSV")
            return None

        base_name = self._get_base_filename()

        # Guardar informacion de la app
        if not info_df.empty:
            info_path = os.path.join(output_dir, f"{base_name}_info.csv")
            info_df.to_csv(info_path, index=False, encoding="utf-8-sig")
            print(f"Informacion guardada en: {info_path}")

        # Guardar reviews
        reviews_path = os.path.join(output_dir, f"{base_name}_reviews.csv")
        reviews_df.to_csv(reviews_path, index=False, encoding="utf-8-sig")

        print(f"CSV guardado en: {reviews_path}")
        return reviews_path

    def to_excel(self, output_dir: Optional[str] = None) -> Optional[str]:
        """
        Exporta los datos a Excel con formato profesional.

        Incluye dos hojas: Reviews y App_Info.
        Ajusta automaticamente el ancho de las columnas.

        Args:
            output_dir: Directorio de salida (usa el de config si no se especifica)

        Returns:
            Ruta del archivo Excel, o None si falla.
        """
        output_dir = output_dir or self.config.output_dir
        self._ensure_output_dir(output_dir)

        info_df, reviews_df = self.to_dataframe()

        if reviews_df.empty:
            print("No hay datos para exportar a Excel")
            return None

        base_name = self._get_base_filename()
        excel_path = os.path.join(output_dir, f"{base_name}_reviews.xlsx")

        try:
            with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
                # Hoja de reviews
                reviews_df.to_excel(writer, sheet_name="Reviews", index=False)

                # Ajustar ancho de columnas automaticamente
                worksheet = writer.sheets["Reviews"]
                for idx, column in enumerate(reviews_df.columns, 1):
                    # Calcular ancho maximo entre el contenido y el encabezado
                    content_width = reviews_df[column].astype(str).map(len).max()
                    header_width = len(column)
                    max_len = max(content_width, header_width) + 2
                    # Limitar ancho maximo a 50 caracteres
                    max_len = min(max_len, 50)
                    col_letter = get_column_letter(idx)
                    worksheet.column_dimensions[col_letter].width = max_len

                # Hoja de informacion de la app
                if not info_df.empty:
                    info_df.to_excel(writer, sheet_name="App_Info", index=False)

            print(f"Excel guardado en: {excel_path}")
            return excel_path

        except Exception as e:
            print(f"Error al guardar Excel: {e}")
            return None

    def export_all(self, output_dir: Optional[str] = None) -> Dict[str, Optional[str]]:
        """
        Exporta todos los datos en los formatos configurados.

        Args:
            output_dir: Directorio de salida

        Returns:
            Diccionario con las rutas de los archivos generados.
        """
        output_dir = output_dir or self.config.output_dir
        self._ensure_output_dir(output_dir)

        results = {
            "csv": None,
            "excel": None,
        }

        if self.config.export_csv:
            results["csv"] = self.to_csv(output_dir)

        if self.config.export_excel:
            results["excel"] = self.to_excel(output_dir)

        return results