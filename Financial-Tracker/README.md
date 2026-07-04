# 💰 Financial Tracker - App de Finanzas Personales

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deployed](https://img.shields.io/badge/Deployed-Streamlit-brightgreen.svg)](https://portafolio-financialtrakerdr.streamlit.app/)

> Una aplicación web para gestionar finanzas personales con análisis visual y persistencia de datos.

## 🌐 Demo en vivo

[🔗 Ver demo en Streamlit Cloud](https://portafolio-financialtrakerdr.streamlit.app/)

## 📸 Capturas de Pantalla

### Dashboard Principal
![Dashboard Principal](images/Resumen.PNG)

### Análisis de Gastos
![Análisis de Gastos](images/Analisis%20de%20Gastos.PNG)

### Gestión de Movimientos
![Gestión de Movimientos](images/Movimientos-csv-excel.PNG)

## ✨ Características

- ✅ **Registro de transacciones** - Ingresos y gastos con validación
- 📊 **Dashboard interactivo** - KPIs en tiempo real
- 📈 **Gráficos dinámicos** - Distribución y evolución de gastos
- 🔍 **Filtros avanzados** - Por categoría y rango de fechas
- 💾 **Persistencia automática** - Datos guardados en CSV
- 📥 **Importación masiva** - Desde CSV
- 📤 **Exportación profesional** - A CSV y Excel
- 📱 **Responsive** - Funciona en móvil y desktop

## 🛠️ Tecnologías Usadas

| Tecnología | Uso |
|------------|-----|
| **Python 3.10+** | Lenguaje base |
| **Streamlit** | UI y despliegue |
| **Pandas** | Procesamiento de datos |
| **Plotly** | Gráficos interactivos |
| **Pytest** | Testing unitario |
| **XlsxWriter** | Exportación a Excel |

## 📦 Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/DESOLADORA666/Portafolio.git
cd Portafolio/financial-tracker

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
# Copiar variables de entorno
cp .env.example .env

# Ejecutar aplicación
streamlit run app.py
