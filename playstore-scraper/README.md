# Play Store Scraper – Extracción de Reviews y Datos de Apps

Scraper profesional para extraer información pública de Google Play Store, incluyendo reviews, calificaciones, nombres de usuarios, fechas y versiones de apps. Incluye dashboard interactivo para visualizar los datos.

## 📊 Ejemplo: Duolingo (600 reviews extraídas)

Los datos incluidos en la carpeta `data/` corresponden a reviews de la app Duolingo, extraídas con este scraper. Puedes visualizarlos en el dashboard o analizarlos con Pandas.

## 🚀 Características

- Extrae metadatos de apps (nombre, desarrollador, categoría, rating, descargas, etc.).
- Extrae hasta 500+ reviews con: usuario, texto, calificación, fecha, versión y “me gusta”.
- Exporta a CSV y Excel con formato limpio (columnas ajustadas).
- Dashboard interactivo con Streamlit para visualizar:
  - Métricas clave (total reviews, rating promedio, usuarios únicos).
  - Distribución de calificaciones.
  - Análisis de sentimiento.
  - Evolución de reviews en el tiempo.
  - Palabras más frecuentes.
  - Usuarios más activos.
- Código modular, testeable y con manejo de errores.
- Listo para ejecutar con cualquier `app_id` de Google Play.

## 🛠️ Tecnologías

- Python 3.10+
- google-play-scraper
- Pandas
- Streamlit
- Plotly
- Pytest
- OpenPyXL

## 📦 Instalación

```bash
git clone https://github.com/DESOLADORA666/Portafolio.git
cd Portafolio/playstore-scraper
pip install -r requirements.txt


## 📊 Datos de ejemplo (Duolingo)

La carpeta `data/` contiene un conjunto de 100 reviews extraídas de Duolingo. Los nombres de usuario han sido anonimizados para proteger la privacidad. Puedes usar este archivo para probar el dashboard sin necesidad de ejecutar el scraper.





📸 Capturas de pantalla
Dashboard de métricas y distribución
https://images/dashboard_metrics.png

Análisis de sentimiento y evolución temporal
https://images/sentiment_evolution.png

Palabras clave y usuarios activos
https://images/top_keywords.png

Tabla de datos extraídos
https://images/data_table.png