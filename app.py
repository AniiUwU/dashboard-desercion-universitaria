import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard: Deserción Universitaria", page_icon="🐱", layout="wide")
st.title("🎓 Análisis de Deserción Universitaria")
st.markdown("Dashboard interactivo para la toma de decisiones académicas.")

# Cargar los datos
@st.cache_data
def cargar_datos():
    return pd.read_csv('dataset_personal.csv')

df_original = cargar_datos()

# ==========================================
# NUEVO: MENÚ LATERAL INTERACTIVO (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Filtros de Análisis")
st.sidebar.write("Personaliza la vista del dashboard:")

# Filtro por Nivel Socioeconómico
filtro_nivel = st.sidebar.multiselect(
    "Selecciona Nivel Socioeconómico:",
    options=df_original['nivel_socioeconomico'].unique(),
    default=df_original['nivel_socioeconomico'].unique()
)

# Aplicar el filtro a los datos
if not filtro_nivel:
    df = df_original.copy()
else:
    df = df_original[df_original['nivel_socioeconomico'].isin(filtro_nivel)]

st.sidebar.divider()
st.sidebar.info("🐱 Dashboard diseñado para el Laboratorio 14.")

# ==========================================
# VISUALIZACIONES
# ==========================================
st.header("1. Indicadores y Visualizaciones")

# VISUALIZACIÓN 1: Indicador KPI
tasa_desercion = (df['desercion'].mean() * 100).round(2)
st.metric(label="Tasa Histórica de Deserción (Filtrada)", value=f"{tasa_desercion}%", delta="Riesgo Moderado", delta_color="inverse")

# Fila 1 de gráficos
col1, col2 = st.columns(2)

with col1:
    # VISUALIZACIÓN 2: Gráfico comparativo (Barras)
    st.subheader("Deserción por Nivel Socioeconómico")
    df_agrupado = df.groupby('nivel_socioeconomico')['desercion'].mean().reset_index()
    df_agrupado['desercion'] = df_agrupado['desercion'] * 100
    fig_barras = px.bar(df_agrupado, x='nivel_socioeconomico', y='desercion', 
                        labels={'desercion': 'Tasa de Deserción (%)', 'nivel_socioeconomico': 'Nivel'},
                        color='nivel_socioeconomico', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_barras, use_container_width=True)

with col2:
    # VISUALIZACIÓN NUEVA (BONUS): Gráfico Donut
    st.subheader("Proporción del Estado Actual")
    df_estado = df['desercion'].map({0: 'Continúa', 1: 'Desertó'}).value_counts().reset_index()
    df_estado.columns = ['Estado', 'Cantidad']
    fig_pie = px.pie(df_estado, values='Cantidad', names='Estado', hole=0.4,
                     color_discrete_sequence=['#FF99CC', '#99CCFF'])
    st.plotly_chart(fig_pie, use_container_width=True)

# Fila 2 de gráficos
col3, col4 = st.columns(2)

with col3:
    # VISUALIZACIÓN 3: Distribución estadística (Boxplot)
    st.subheader("Promedio de Notas vs Deserción")
    fig_box = px.box(df, x='desercion', y='promedio_notas', 
                     labels={'desercion': 'Estado (0=Continúa, 1=Desertó)', 'promedio_notas': 'Promedio Académico'},
                     color='desercion', category_orders={"desercion": [0, 1]})
    st.plotly_chart(fig_box, use_container_width=True)

with col4:
    # VISUALIZACIÓN 4: Visualización libre (Scatter Plot)
    st.subheader("Impacto del Trabajo y la Asistencia")
    fig_scatter = px.scatter(df, x='asistencia_pct', y='horas_trabajo_semanal', color='desercion', 
                             size='carga_estres',
                             labels={'asistencia_pct': 'Asistencia (%)', 'horas_trabajo_semanal': 'Horas de Trabajo'})
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ==========================================
# STORYTELLING DE DATOS
# ==========================================
st.header("2. Storytelling de Datos: Conclusiones y Decisiones")
colA, colB = st.columns(2)
with colA:
    st.success("📌 Hallazgos Principales")
    st.markdown("""
    1. **Hallazgo 1 (Alerta Temprana):** Existe una relación directa entre el decaimiento de la asistencia y el incremento del abandono.
    2. **Hallazgo 2 (Estrés Laboral):** Jornadas laborales extensas merman críticamente la asistencia, disparando el estrés.
    """)
with colB:
    st.info("💡 Recomendaciones Organizacionales")
    st.markdown("""
    1. **Recomendación 1:** Desplegar el modelo Random Forest para identificar perfiles en riesgo.
    2. **Recomendación 2:** Diseñar horarios flexibles para estudiantes que acrediten jornadas laborales de tiempo completo.
    """)
