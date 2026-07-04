# 💰 Financial Tracker

> Una aplicación web para gestionar finanzas personales con análisis visual y persistencia de datos.

## 🚀 Características

- ✅ Registro de ingresos y gastos con validación
- 📊 Dashboard con KPIs en tiempo real
- 📈 Gráficos interactivos con Plotly
- 🔍 Filtros por categoría y rango de fechas
- 💾 Persistencia automática en CSV
- 📥 Importación de datos desde CSV
- 📤 Exportación a CSV y Excel
- 📱 Interfaz responsive

## 🛠️ Tecnologías

- **Python 3.10+**
- **Streamlit** - UI
- **Pandas** - Procesamiento de datos
- **Plotly** - Visualización interactiva
- **Pytest** - Testing

## 📦 Instalación

```bash
# Clonar repositorio
git clone https://github.com/DESOLADORA666/finanzas-tracker.git
cd finanzas-tracker

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env

# Ejecutar aplicación
streamlit run app.py
