"""
Modulo scraper - Extrae datos publicos de Google Play Store.

Utiliza la libreria google-play-scraper para obtener informacion
de apps y sus reviews de manera programatica.
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from google_play_scraper import Sort, app, reviews, reviews_all

from config.settings import ScraperConfig

# Configurar logging para seguimiento de ejecucion
logger = logging.getLogger(__name__)


class PlayStoreScraper:
    """
    Scraper para Google Play Store.

    Extrae informacion publica de una app y sus reviews.
    Incluye manejo de errores, rate limiting y paginacion.

    Attributes:
        config: Configuracion del scraper
        app_info: Diccionario con informacion de la app
        reviews_data: Lista de diccionarios con las reviews
        timestamp: Marca de tiempo de la ejecucion
    """

    def __init__(self, config: Optional[ScraperConfig] = None):
        """
        Inicializa el scraper con la configuracion proporcionada.

        Args:
            config: Configuracion del scraper. Si no se proporciona,
                    se usa la configuracion por defecto.
        """
        self.config = config or ScraperConfig()
        self.app_info: Optional[Dict] = None
        self.reviews_data: List[Dict] = []
        self.timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    def get_app_info(self) -> Optional[Dict]:
        """
        Extrae la informacion publica de la app.

        Realiza una peticion a la API de Google Play Store para
        obtener los metadatos de la aplicacion.

        Returns:
            Diccionario con la informacion de la app,
            o None si ocurre un error.
        """
        logger.info(f"Obteniendo informacion de: {self.config.app_id}")

        try:
            info = app(
                self.config.app_id,
                lang=self.config.lang,
                country=self.config.country
            )

            self.app_info = {
                "app_id": self.config.app_id,
                "app_name": info.get("title", "N/A"),
                "developer": info.get("developer", "N/A"),
                "category": info.get("genre", "N/A"),
                "rating": info.get("score", 0.0),
                "reviews_count": info.get("reviews", 0),
                "installs": info.get("installs", "N/A"),
                "price": info.get("price", 0.0),
                "description": info.get("description", "N/A")[:500] + "...",
                "updated": info.get("updated", "N/A"),
                "android_version": info.get("androidVersion", "N/A"),
                "content_rating": info.get("contentRating", "N/A"),
                "url": f"https://play.google.com/store/apps/details?id={self.config.app_id}"
            }

            logger.info(f"App encontrada: {self.app_info['app_name']}")
            return self.app_info

        except Exception as e:
            logger.error(f"Error al obtener informacion: {e}")
            return None

    def _process_review(self, review: Dict) -> Dict:
        """
        Procesa una review cruda para estandarizar su formato.

        Limpia el texto, formatea la fecha y extrae los campos relevantes.

        Args:
            review: Diccionario con datos crudos de la review

        Returns:
            Diccionario con la review procesada y estandarizada.
        """
        # Procesar fecha: convertir a string o usar valor por defecto
        date_value = review.get("at")
        if date_value:
            date_str = date_value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            date_str = "N/A"

        # Limpiar texto de la review (eliminar saltos de linea)
        content = review.get("content", "")
        clean_content = content.replace("\n", " ").strip()

        # Procesar respuesta del desarrollador si existe
        reply = review.get("replyContent")
        clean_reply = reply.replace("\n", " ").strip() if reply else "N/A"

        return {
            "user_name": review.get("userName", "Anonimo"),
            "review_text": clean_content,
            "rating": review.get("score", 0),
            "date": date_str,
            "version": review.get("reviewCreatedVersion", "N/A"),
            "thumbs_up": review.get("thumbsUpCount", 0),
            "reply": clean_reply
        }

    def get_reviews_paginated(self, count: int = 500) -> List[Dict]:
        """
        Extrae reviews usando paginacion y manejo de errores.

        Realiza peticiones paginadas hasta alcanzar el numero
        solicitado de reviews o hasta que no haya mas paginas.

        Args:
            count: Numero maximo de reviews a extraer

        Returns:
            Lista de diccionarios con las reviews procesadas.
        """
        logger.info(f"Extrayendo {count} reviews de: {self.config.app_id}")

        all_reviews = []
        retry_count = 0
        result = None
        token = None

        while len(all_reviews) < count and retry_count < self.config.max_retries:
            try:
                # Primera pagina o pagina con continuation token
                if token is None:
                    result, token = reviews(
                        self.config.app_id,
                        lang=self.config.lang,
                        country=self.config.country,
                        sort=Sort.NEWEST,
                        count=min(200, count - len(all_reviews))
                    )
                else:
                    result, token = reviews(
                        self.config.app_id,
                        continuation_token=token
                    )

                # Procesar cada review de la pagina
                for review in result:
                    all_reviews.append(self._process_review(review))

                logger.info(f"Progreso: {len(all_reviews)}/{count} reviews")

                # Pausa para evitar rate limiting
                time.sleep(self.config.sleep_seconds)

                # Si no hay mas paginas, salir del bucle
                if token is None:
                    break

            except Exception as e:
                retry_count += 1
                logger.warning(f"Error en extraccion (intento {retry_count}): {e}")
                # Esperar mas tiempo si hay error
                time.sleep(5)

        self.reviews_data = all_reviews
        logger.info(f"Se extrajeron {len(all_reviews)} reviews")
        return all_reviews

    def get_reviews_bulk(self, max_reviews: int = 500) -> List[Dict]:
        """
        Extrae reviews usando el metodo bulk de la libreria.

        Es mas eficiente que la paginacion manual pero puede
        ser mas agresivo con el rate limiting.

        Args:
            max_reviews: Limite maximo de reviews a extraer

        Returns:
            Lista de diccionarios con las reviews procesadas.
        """
        logger.info(f"Extrayendo todas las reviews (max: {max_reviews})")

        try:
            # Usar reviews_all que es mas eficiente
            result = reviews_all(
                self.config.app_id,
                lang=self.config.lang,
                country=self.config.country,
                sleep_milliseconds=500
            )

            # Limitar la cantidad de reviews
            result = result[:max_reviews]

            # Procesar cada review
            for review in result:
                self.reviews_data.append(self._process_review(review))

            logger.info(f"Se extrajeron {len(self.reviews_data)} reviews")
            return self.reviews_data

        except Exception as e:
            logger.error(f"Error en extraccion masiva: {e}")
            # Fallback al metodo paginado
            return self.get_reviews_paginated(count=max_reviews)

    def get_reviews(self, max_reviews: int = 500) -> List[Dict]:
        """
        Metodo principal para extraer reviews.

        Usa paginacion por defecto para evitar bloqueos del metodo bulk.

        Args:
            max_reviews: Numero maximo de reviews a extraer

        Returns:
            Lista de diccionarios con las reviews procesadas.
        """
        return self.get_reviews_paginated(count=max_reviews)

    def get_summary(self) -> Dict:
        """
        Genera un resumen estadistico de los datos extraidos.

        Calcula metricas como promedio de calificacion,
        distribucion de estrellas y total de reviews.

        Returns:
            Diccionario con las metricas resumidas.
        """
        summary: Dict = {
            "app_name": "N/A",
            "app_id": self.config.app_id,
            "total_reviews": len(self.reviews_data),
        }

        # Agregar informacion de la app si esta disponible
        if self.app_info:
            summary.update({
                "app_name": self.app_info.get("app_name", "N/A"),
                "developer": self.app_info.get("developer", "N/A"),
                "category": self.app_info.get("category", "N/A"),
                "rating": self.app_info.get("rating", 0.0),
                "installs": self.app_info.get("installs", "N/A"),
            })

        # Calcular estadisticas de las reviews
        if self.reviews_data:
            ratings = [r["rating"] for r in self.reviews_data if r["rating"] > 0]
            if ratings:
                summary["avg_rating"] = round(sum(ratings) / len(ratings), 2)
                summary["five_stars"] = ratings.count(5)
                summary["four_stars"] = ratings.count(4)
                summary["three_stars"] = ratings.count(3)
                summary["two_stars"] = ratings.count(2)
                summary["one_star"] = ratings.count(1)
                summary["positive_pct"] = round(
                    (ratings.count(4) + ratings.count(5)) / len(ratings) * 100, 2
                )
                summary["negative_pct"] = round(
                    (ratings.count(1) + ratings.count(2)) / len(ratings) * 100, 2
                )

        return summary

    def print_summary(self) -> None:
        """Muestra un resumen formateado en la consola."""
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print("RESUMEN DE EXTRACCION")
        print("=" * 60)
        print(f"App: {summary.get('app_name', 'N/A')}")
        print(f"ID: {summary.get('app_id', 'N/A')}")
        print(f"Desarrollador: {summary.get('developer', 'N/A')}")
        print(f"Categoria: {summary.get('category', 'N/A')}")
        print(f"Rating: {summary.get('rating', 'N/A')}")
        print(f"Descargas: {summary.get('installs', 'N/A')}")
        print(f"\nReviews extraidas: {summary.get('total_reviews', 0)}")

        if "avg_rating" in summary:
            print(f"Rating promedio: {summary['avg_rating']:.2f}")
            print(f"Reviews con 5 estrellas: {summary.get('five_stars', 0)}")
            print(f"Reviews con 1 estrella: {summary.get('one_star', 0)}")
            print(f"Reviews positivas (4-5): {summary.get('positive_pct', 0):.1f}%")
            print(f"Reviews negativas (1-2): {summary.get('negative_pct', 0):.1f}%")

        print("=" * 60)

    def run(self) -> Dict[str, Optional[Dict]]:
        """
        Ejecuta el scraper completo.

        Obtiene la informacion de la app y extrae las reviews.
        Es el metodo principal que debe llamarse desde el exterior.

        Returns:
            Diccionario con app_info y reviews_data.
        """
        logger.info(f"Iniciando scraper para: {self.config.app_id}")

        # Obtener informacion de la app
        self.get_app_info()

        if not self.app_info:
            logger.error("No se pudo obtener informacion de la app")
            return {"app_info": None, "reviews": []}

        # Extraer reviews
        self.get_reviews(max_reviews=self.config.max_reviews)

        # Mostrar resumen
        self.print_summary()

        return {
            "app_info": self.app_info,
            "reviews": self.reviews_data
        }