"""
Dashboard de Streamlit para visualizar datos de Google Play Store.

Permite cargar archivos CSV o Excel con datos de reviews
y visualizar metricas, graficos y analisis de sentimiento.
"""

import os
import sys

# Agregar el directorio raiz al path para importar modulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.settings import DEFAULT_DASHBOARD_CONFIG
from src.analyzer import Analyzer


# Configuracion de la pagina
st.set_page_config(
    page_title=DEFAULT_DASHBOARD_CONFIG.page_title,
    page_icon=DEFAULT_DASHBOARD_CONFIG.page_icon,
    layout=DEFAULT_DASHBOARD_CONFIG.layout
)


def load_data(uploaded_file) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV o Excel.

    Args:
        uploaded_file: Archivo subido a Streamlit

    Returns:
        DataFrame con los datos cargados
    """
    if uploaded_file is None:
        return pd.DataFrame()

    try:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "csv":
            df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        elif file_extension in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file, sheet_name="Reviews")
        else:
            st.error(f"Formato no soportado: {file_extension}")
            return pd.DataFrame()

        return df

    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()


def show_metrics(df: pd.DataFrame) -> None:
    """
    Muestra metricas clave en el dashboard.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    stats = analyzer.get_summary_stats()
    sentiment = analyzer.get_sentiment_distribution()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Reviews",
            value=stats.get("total_reviews", 0)
        )

    with col2:
        st.metric(
            label="Rating Promedio",
            value=f"{stats.get('avg_rating', 0):.2f} ⭐"
        )

    with col3:
        st.metric(
            label="Usuarios Unicos",
            value=stats.get("unique_users", 0)
        )

    with col4:
        positivo = sentiment.get("positivo", 0)
        st.metric(
            label="Sentimiento Positivo",
            value=f"{positivo:.1f}%"
        )


def show_rating_distribution(df: pd.DataFrame) -> None:
    """
    Muestra grafico de distribucion de calificaciones.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    distribution = analyzer.get_rating_distribution()

    if not distribution:
        return

    fig = px.bar(
        x=list(distribution.keys()),
        y=list(distribution.values()),
        labels={"x": "Calificacion", "y": "Cantidad"},
        title="Distribucion de Calificaciones",
        color=list(distribution.keys()),
        color_continuous_scale="Blues"
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def show_sentiment_distribution(df: pd.DataFrame) -> None:
    """
    Muestra grafico de distribucion de sentimiento.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    sentiment = analyzer.get_sentiment_distribution()

    if not sentiment:
        return

    colors = {"positivo": "#2ecc71", "neutral": "#f1c40f", "negativo": "#e74c3c"}

    fig = go.Figure(data=[
        go.Pie(
            labels=list(sentiment.keys()),
            values=list(sentiment.values()),
            marker_colors=[colors[k] for k in sentiment.keys()],
            textinfo="label+percent",
            hole=0.4
        )
    ])

    fig.update_layout(title="Distribucion de Sentimiento")
    st.plotly_chart(fig, use_container_width=True)


def show_reviews_over_time(df: pd.DataFrame) -> None:
    """
    Muestra grafico de reviews en el tiempo.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    reviews_by_date = analyzer.get_reviews_by_date()

    if not reviews_by_date:
        return

    # Convertir a DataFrame y ordenar por fecha
    df_dates = pd.DataFrame(
        list(reviews_by_date.items()),
        columns=["Fecha", "Cantidad"]
    )
    df_dates["Fecha"] = pd.to_datetime(df_dates["Fecha"])
    df_dates = df_dates.sort_values("Fecha")

    fig = px.line(
        df_dates,
        x="Fecha",
        y="Cantidad",
        title="Evolucion de Reviews en el Tiempo",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Cantidad de Reviews"
    )

    st.plotly_chart(fig, use_container_width=True)


def show_top_keywords(df: pd.DataFrame) -> None:
    """
    Muestra las palabras mas frecuentes en las reviews.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    keywords = analyzer.get_top_keywords(n=20)

    if not keywords:
        return

    words, counts = zip(*keywords)

    fig = px.bar(
        x=list(words),
        y=list(counts),
        labels={"x": "Palabra", "y": "Frecuencia"},
        title="Palabras mas Frecuentes en Reviews",
        color=list(counts),
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def show_user_activity(df: pd.DataFrame) -> None:
    """
    Muestra los usuarios mas activos.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    users = analyzer.get_user_activity(top_n=10)

    if not users:
        return

    users_list, counts = zip(*users)

    fig = px.bar(
        x=list(users_list),
        y=list(counts),
        labels={"x": "Usuario", "y": "Reviews"},
        title="Usuarios mas Activos",
        color=list(counts),
        color_continuous_scale="Oranges"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def show_daily_activity(df: pd.DataFrame) -> None:
    """
    Muestra la actividad por dia de la semana.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        return

    analyzer = Analyzer(df.to_dict("records"))
    activity = analyzer.get_daily_activity()

    if not activity:
        return

    # Ordenar los dias de la semana
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"]

    # Reordenar
    ordered_activity = {
        day: activity.get(day, 0) for day in days_order
    }

    fig = px.bar(
        x=list(ordered_activity.keys()),
        y=list(ordered_activity.values()),
        labels={"x": "Dia de la Semana", "y": "Reviews"},
        title="Actividad por Dia de la Semana",
        color=list(ordered_activity.values()),
        color_continuous_scale="Teal"
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def show_raw_data(df: pd.DataFrame) -> None:
    """
    Muestra los datos crudos en una tabla.

    Args:
        df: DataFrame con los datos
    """
    if df.empty:
        st.info("No hay datos para mostrar")
        return

    st.subheader("Datos Completos")

    # Limitar a 1000 filas para rendimiento
    if len(df) > 1000:
        st.warning(f"Mostrando 1000 de {len(df)} filas")
        display_df = df.head(1000)
    else:
        display_df = df

    st.dataframe(display_df, use_container_width=True)


def main():
    """Funcion principal del dashboard."""
    st.title(f"{DEFAULT_DASHBOARD_CONFIG.icon} {DEFAULT_DASHBOARD_CONFIG.title}")

    st.markdown("""
    Sube un archivo CSV o Excel con datos de reviews de Google Play Store
    para visualizar metricas, graficos y analisis de sentimiento.
    """)

    # Sidebar para carga de archivos
    with st.sidebar:
        st.header("Carga de Datos")

        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV o Excel",
            type=["csv", "xlsx", "xls"],
            help="El archivo debe tener columnas: user_name, review_text, rating, date, version, thumbs_up, reply"
        )

        if uploaded_file:
            st.success(f"Archivo cargado: {uploaded_file.name}")

            # Mostrar informacion del archivo
            file_details = {
                "Nombre": uploaded_file.name,
                "Tamaño": f"{uploaded_file.size / 1024:.2f} KB",
                "Tipo": uploaded_file.type
            }
            st.json(file_details)

        st.divider()

        st.header("Ejemplos de Apps")
        st.caption("Puedes usar el scraper para obtener datos de estas apps:")

        apps = [
            "com.whatsapp - WhatsApp",
            "com.instagram.android - Instagram",
            "com.spotify.music - Spotify",
            "com.netflix.mediaclient - Netflix",
            "com.duolingo - Duolingo"
        ]

        for app in apps:
            st.code(app, language="text")

    # Cargar y procesar datos
    if uploaded_file is None:
        st.info("👈 Sube un archivo en el panel lateral para comenzar")
        return

    df = load_data(uploaded_file)

    if df.empty:
        st.warning("No se pudieron cargar los datos. Verifica el formato del archivo.")
        return

    # Validar columnas requeridas
    required_columns = ["user_name", "review_text", "rating", "date"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Columnas faltantes: {', '.join(missing_columns)}")
        st.info("El archivo debe tener las columnas: user_name, review_text, rating, date")
        return

    # Mostrar metricas
    show_metrics(df)

    st.divider()

    # Graficos principales
    col1, col2 = st.columns(2)

    with col1:
        show_rating_distribution(df)

    with col2:
        show_sentiment_distribution(df)

    # Graficos secundarios
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        show_reviews_over_time(df)

    with col2:
        show_daily_activity(df)

    # Graficos adicionales
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        show_top_keywords(df)

    with col2:
        show_user_activity(df)

    # Datos crudos
    st.divider()
    show_raw_data(df)


if __name__ == "__main__":
    main()