"""
Tests para el modulo scraper.

Prueba la funcionalidad de extraccion de datos
de Google Play Store.
"""

import os
import tempfile

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

import pandas as pd

from config.settings import ScraperConfig
from src.scraper import PlayStoreScraper
from src.exporter import Exporter


class TestPlayStoreScraper:
    """Pruebas para la clase PlayStoreScraper."""

    def test_init_with_default_config(self):
        """Verifica que el scraper se inicializa con la configuracion por defecto."""
        scraper = PlayStoreScraper()
        assert scraper.config is not None
        assert scraper.config.app_id == "com.whatsapp"
        assert scraper.config.lang == "es"
        assert scraper.config.country == "mx"

    def test_init_with_custom_config(self):
        """Verifica que el scraper se inicializa con configuracion personalizada."""
        config = ScraperConfig(
            app_id="com.instagram.android",
            lang="en",
            country="us"
        )
        scraper = PlayStoreScraper(config)
        assert scraper.config.app_id == "com.instagram.android"
        assert scraper.config.lang == "en"
        assert scraper.config.country == "us"

    def test_process_review(self):
        """Verifica el procesamiento de una review cruda."""
        scraper = PlayStoreScraper()

        raw_review = {
            "userName": "test_user",
            "content": "Excelente aplicacion\nMuy util",
            "score": 5,
            "at": datetime(2025, 1, 15, 10, 30, 0),
            "reviewCreatedVersion": "1.0.0",
            "thumbsUpCount": 10,
            "replyContent": "Gracias por tu review"
        }

        processed = scraper._process_review(raw_review)

        assert processed["user_name"] == "test_user"
        assert processed["review_text"] == "Excelente aplicacion Muy util"
        assert processed["rating"] == 5
        assert processed["date"] == "2025-01-15 10:30:00"
        assert processed["version"] == "1.0.0"
        assert processed["thumbs_up"] == 10
        assert processed["reply"] == "Gracias por tu review"

    def test_process_review_without_reply(self):
        """Verifica el procesamiento de una review sin respuesta del desarrollador."""
        scraper = PlayStoreScraper()

        raw_review = {
            "userName": "test_user",
            "content": "Buena app",
            "score": 4,
            "at": datetime(2025, 1, 15, 10, 30, 0),
            "reviewCreatedVersion": "1.0.0",
            "thumbsUpCount": 5,
            "replyContent": None
        }

        processed = scraper._process_review(raw_review)
        assert processed["reply"] == "N/A"

    def test_get_summary_empty(self):
        """Verifica que get_summary maneja el caso sin datos."""
        scraper = PlayStoreScraper()
        scraper.reviews_data = []

        summary = scraper.get_summary()
        assert summary["app_id"] == "com.whatsapp"
        assert summary["total_reviews"] == 0

    @patch("src.scraper.app")
    def test_get_app_info_success(self, mock_app):
        """Verifica la obtencion exitosa de informacion de la app."""
        mock_app.return_value = {
            "title": "Test App",
            "developer": "Test Developer",
            "genre": "Test Category",
            "score": 4.5,
            "reviews": 1000,
            "installs": "100,000+",
            "price": 0.0,
            "description": "Test description",
            "updated": "2025-01-01",
            "androidVersion": "5.0",
            "contentRating": "Everyone"
        }

        scraper = PlayStoreScraper()
        result = scraper.get_app_info()

        assert result is not None
        assert result["app_name"] == "Test App"
        assert result["developer"] == "Test Developer"
        assert result["rating"] == 4.5

    @patch("src.scraper.app")
    def test_get_app_info_failure(self, mock_app):
        """Verifica el manejo de errores al obtener informacion de la app."""
        mock_app.side_effect = Exception("Network error")

        scraper = PlayStoreScraper()
        result = scraper.get_app_info()

        assert result is None
        assert scraper.app_info is None


class TestScraperConfig:
    """Pruebas para la configuracion del scraper."""

    def test_config_default_values(self):
        """Verifica los valores por defecto de la configuracion."""
        config = ScraperConfig()
        assert config.app_id == "com.whatsapp"
        assert config.lang == "es"
        assert config.country == "mx"
        assert config.max_reviews == 500
        assert config.sleep_seconds == 2
        assert config.max_retries == 3

    def test_config_custom_values(self):
        """Verifica que se pueden personalizar los valores de configuracion."""
        config = ScraperConfig(
            app_id="com.test.app",
            lang="fr",
            country="fr",
            max_reviews=100,
            sleep_seconds=5,
            max_retries=1
        )
        assert config.app_id == "com.test.app"
        assert config.lang == "fr"
        assert config.country == "fr"
        assert config.max_reviews == 100
        assert config.sleep_seconds == 5
        assert config.max_retries == 1


class TestExporter:
    """Pruebas para la clase Exporter."""

    def setup_method(self):
        """Configura un scraper con datos de prueba."""
        self.config = ScraperConfig(app_id="com.test.app")
        self.scraper = PlayStoreScraper(self.config)

        # Datos de prueba
        self.scraper.app_info = {
            "app_id": "com.test.app",
            "app_name": "Test App",
            "developer": "Test Developer",
            "category": "Test Category",
            "rating": 4.5,
            "reviews_count": 100,
            "installs": "1,000+",
            "price": 0.0,
            "description": "Test description...",
            "updated": "2025-01-01"
        }

        self.scraper.reviews_data = [
            {
                "user_name": "user1",
                "review_text": "Excelente app",
                "rating": 5,
                "date": "2025-01-01 10:00:00",
                "version": "1.0",
                "thumbs_up": 10,
                "reply": "Gracias"
            },
            {
                "user_name": "user2",
                "review_text": "Buena app",
                "rating": 4,
                "date": "2025-01-02 11:00:00",
                "version": "1.0",
                "thumbs_up": 5,
                "reply": "N/A"
            }
        ]

        self.exporter = Exporter(self.scraper)

    def test_init(self):
        """Verifica la inicializacion del exporter."""
        assert self.exporter.scraper is not None
        assert self.exporter.app_info is not None
        assert len(self.exporter.reviews) == 2
        assert self.exporter.app_id_clean == "com_test_app"

    def test_to_dataframe(self):
        """Verifica la conversion a DataFrame."""
        info_df, reviews_df = self.exporter.to_dataframe()

        assert not info_df.empty
        assert info_df.iloc[0]["app_name"] == "Test App"

        assert not reviews_df.empty
        assert len(reviews_df) == 2
        assert reviews_df.iloc[0]["user_name"] == "user1"

    def test_to_csv(self):
        """Verifica la exportacion a CSV."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self.config.output_dir = tmpdir
            result = self.exporter.to_csv(tmpdir)

            assert result is not None
            assert os.path.exists(result)

            # Verificar contenido del CSV
            df = pd.read_csv(result, encoding="utf-8-sig")
            assert len(df) == 2
            assert df.iloc[0]["user_name"] == "user1"

    def test_to_excel(self):
        """Verifica la exportacion a Excel."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self.config.output_dir = tmpdir
            result = self.exporter.to_excel(tmpdir)

            assert result is not None
            assert os.path.exists(result)
            assert result.endswith(".xlsx")

    def test_export_all(self):
        """Verifica la exportacion en todos los formatos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self.config.output_dir = tmpdir
            results = self.exporter.export_all(tmpdir)

            assert results["csv"] is not None
            assert results["excel"] is not None
            assert os.path.exists(results["csv"])
            assert os.path.exists(results["excel"])

    def test_empty_reviews(self):
        """Verifica el manejo de exporters sin reviews."""
        self.scraper.reviews_data = []
        exporter = Exporter(self.scraper)

        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.to_csv(tmpdir)
            assert result is None

            result = exporter.to_excel(tmpdir)
            assert result is None

    def test_get_base_filename(self):
        """Verifica la generacion del nombre base."""
        base_name = self.exporter._get_base_filename()
        assert base_name.startswith("com_test_app_")
        assert len(base_name) > len("com_test_app_")


class TestExporterConfig:
    """Pruebas para la configuracion del exporter."""

    def test_export_config(self):
        """Verifica que la configuracion de exportacion funciona."""
        config = ScraperConfig(
            app_id="com.test.app",
            export_csv=True,
            export_excel=False
        )

        scraper = PlayStoreScraper(config)
        scraper.app_info = {"app_id": "com.test.app"}
        scraper.reviews_data = [{"user_name": "test", "review_text": "test"}]

        exporter = Exporter(scraper)

        with tempfile.TemporaryDirectory() as tmpdir:
            config.output_dir = tmpdir
            results = exporter.export_all(tmpdir)

            assert results["csv"] is not None
            assert results["excel"] is None
