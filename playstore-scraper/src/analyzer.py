"""
Modulo analyzer - Analisis de datos de Play Store.

Proporciona funciones para analizar y visualizar
los datos extraidos de Google Play Store.
"""

from collections import Counter
from typing import Dict, List, Optional, Tuple

import pandas as pd
import re


class Analyzer:
    """
    Analiza los datos extraidos de Google Play Store.

    Proporciona metodos para analisis de sentimiento,
    distribucion de calificaciones y extraccion de palabras clave.

    Attributes:
        reviews: Lista de diccionarios con las reviews
        df: DataFrame de pandas con las reviews
    """

    # Palabras comunes que se excluyen del analisis
    STOPWORDS = {
        "the", "and", "for", "are", "but", "not", "you", "all",
        "can", "had", "her", "was", "one", "our", "out", "que",
        "con", "para", "por", "una", "como", "mas", "muy", "los",
        "las", "del", "que", "con", "para", "por", "una", "sobre",
        "sin", "ante", "bajo", "tras", "contra", "hasta", "desde",
        "entre", "segun", "durante", "mediante", "a", "ante", "bajo",
        "cabe", "con", "contra", "de", "desde", "durante", "en",
        "entre", "hacia", "hasta", "mediante", "para", "por", "segun",
        "sin", "sobre", "tras", "versus", "via"
    }

    def __init__(self, reviews: List[Dict]):
        """
        Inicializa el analizador con una lista de reviews.

        Args:
            reviews: Lista de diccionarios con las reviews extraidas
        """
        self.reviews = reviews
        self.df = pd.DataFrame(reviews) if reviews else pd.DataFrame()

    def _clean_text(self, text: str) -> str:
        """
        Limpia un texto eliminando caracteres especiales y convirtiendo a minusculas.

        Args:
            text: Texto a limpiar

        Returns:
            Texto limpio
        """
        if not text:
            return ""
        # Eliminar caracteres especiales, mantener letras y espacios
        cleaned = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ ]', ' ', str(text))
        # Convertir a minusculas
        return cleaned.lower().strip()

    def _extract_words(self, text: str) -> List[str]:
        """
        Extrae palabras de un texto eliminando stopwords.

        Args:
            text: Texto del cual extraer palabras

        Returns:
            Lista de palabras significativas
        """
        clean_text = self._clean_text(text)
        words = clean_text.split()
        # Filtrar stopwords y palabras muy cortas
        return [w for w in words if w not in self.STOPWORDS and len(w) > 2]

    def get_rating_distribution(self) -> Dict[int, int]:
        """
        Calcula la distribucion de calificaciones.

        Returns:
            Diccionario con {rating: count}
        """
        if self.df.empty:
            return {}

        ratings = self.df["rating"].value_counts().to_dict()
        # Asegurar que todas las calificaciones 1-5 esten presentes
        for i in range(1, 6):
            ratings.setdefault(i, 0)

        return dict(sorted(ratings.items()))

    def get_top_keywords(self, n: int = 20) -> List[Tuple[str, int]]:
        """
        Obtiene las palabras mas frecuentes en las reviews.

        Args:
            n: Numero de palabras a retornar

        Returns:
            Lista de tuplas (palabra, frecuencia)
        """
        if self.df.empty:
            return []

        all_words = []
        for text in self.df["review_text"].dropna():
            all_words.extend(self._extract_words(text))

        word_counts = Counter(all_words)
        return word_counts.most_common(n)

    def get_sentiment_distribution(self) -> Dict[str, float]:
        """
        Clasifica las reviews por sentimiento basado en la calificacion.

        Retorna:
            Diccionario con porcentajes de sentimiento positivo/neutral/negativo.
        """
        if self.df.empty:
            return {"positivo": 0.0, "neutral": 0.0, "negativo": 0.0}

        total = len(self.df)
        positive = len(self.df[self.df["rating"] >= 4])
        negative = len(self.df[self.df["rating"] <= 2])
        neutral = total - positive - negative

        return {
            "positivo": round((positive / total) * 100, 2),
            "neutral": round((neutral / total) * 100, 2),
            "negativo": round((negative / total) * 100, 2)
        }

    def get_reviews_by_date(self) -> Dict[str, int]:
        """
        Agrupa las reviews por fecha.

        Returns:
            Diccionario con {fecha: cantidad_de_reviews}
        """
        if self.df.empty:
            return {}

        df_copy = self.df.copy()
        df_copy["date_only"] = pd.to_datetime(df_copy["date"]).dt.date
        return df_copy.groupby("date_only").size().to_dict()

    def get_daily_activity(self) -> Dict[str, int]:
        """
        Analiza la actividad por dia de la semana.

        Returns:
            Diccionario con {dia: cantidad_de_reviews}
        """
        if self.df.empty:
            return {}

        df_copy = self.df.copy()
        df_copy["weekday"] = pd.to_datetime(df_copy["date"]).dt.day_name()
        return df_copy.groupby("weekday").size().to_dict()

    def get_user_activity(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Obtiene los usuarios mas activos.

        Args:
            top_n: Numero de usuarios a retornar

        Returns:
            Lista de tuplas (usuario, cantidad_de_reviews)
        """
        if self.df.empty:
            return []

        user_counts = self.df["user_name"].value_counts()
        return user_counts.head(top_n).items()

    def get_summary_stats(self) -> Dict:
        """
        Genera estadisticas resumidas de las reviews.

        Returns:
            Diccionario con estadisticas clave.
        """
        if self.df.empty:
            return {
                "total_reviews": 0,
                "avg_rating": 0,
                "max_rating": 0,
                "min_rating": 0
            }

        return {
            "total_reviews": len(self.df),
            "avg_rating": round(self.df["rating"].mean(), 2),
            "max_rating": self.df["rating"].max(),
            "min_rating": self.df["rating"].min(),
            "unique_users": self.df["user_name"].nunique()
        }