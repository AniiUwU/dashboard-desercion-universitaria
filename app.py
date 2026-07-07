import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard: Deserción Universitaria", layout="wide")
st.set_page_config(page_title="Dashboard: Deserción Universitaria", page_icon="🐱", layout="wide")
st.markdown("Dashboard interactivo para la toma de decisiones académicas.")

# Cargar los datos que generamos en el Paso 4
@st.cache_data
def cargar_datos():
    return pd.read_csv('dataset_personal.csv')

df = cargar_datos()

# ==========================================
# PASO 1: VISUALIZACIONES OBLIGATORIAS
# ==========================================

st.header("1. Indicadores y Visualizaciones")

# VISUALIZACIÓN 1: Indicador KPI [cite: 20]
tasa_desercion = (df['desercion'].mean() * 100).round(2)
st.metric(label="Tasa Histórica de Deserción", value=f"{tasa_desercion}%", delta="Riesgo Moderado", delta_color="inverse")

col1, col2 = st.columns(2)

with col1:
    # VISUALIZACIÓN 2: Gráfico comparativo (Barras) 
    st.subheader("Deserción por Nivel Socioeconómico")
    df_agrupado = df.groupby('nivel_socioeconomico')['desercion'].mean().reset_index()
    df_agrupado['desercion'] = df_agrupado['desercion'] * 100
    fig_barras = px.bar(df_agrupado, x='nivel_socioeconomico', y='desercion', 
                        labels={'desercion': 'Tasa de Deserción (%)', 'nivel_socioeconomico': 'Nivel Socioeconómico'},
                        color='nivel_socioeconomico', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_barras, use_container_width=True)

with col2:
    # VISUALIZACIÓN 3: Distribución estadística (Boxplot) 
    st.subheader("Promedio de Notas vs Deserción")
    fig_box = px.box(df, x='desercion', y='promedio_notas', 
                     labels={'desercion': 'Estado (0=Continúa, 1=Desertó)', 'promedio_notas': 'Promedio Académico'},
                     color='desercion', category_orders={"desercion": [0, 1]})
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# VISUALIZACIÓN 4: Visualización libre (Scatter Plot) 
st.subheader("Impacto del Trabajo y la Asistencia en la Carga de Estrés")
fig_scatter = px.scatter(df, x='asistencia_pct', y='horas_trabajo_semanal', color='desercion', 
                         size='carga_estres', hover_data=['promedio_notas'],
                         labels={'asistencia_pct': 'Asistencia (%)', 'horas_trabajo_semanal': 'Horas de Trabajo Semanal'},
                         title="El tamaño de la burbuja representa la Carga de Estrés calculada")
st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# PASO 2: STORYTELLING DE DATOS 
# ==========================================
st.divider()
st.header("2. Storytelling de Datos: Conclusiones y Decisiones")

col3, col4 = st.columns(2)

with col3:
    st.success("📌 Hallazgos Principales")
    st.markdown("""
    1. **Hallazgo 1 (Alerta Temprana):** Existe una relación directa entre el decaimiento de la asistencia y el incremento del abandono. Los alumnos que bajan del 70% de asistencia son los más propensos a desertar.
    2. **Hallazgo 2 (Estrés Laboral):** El gráfico de dispersión demuestra que jornadas laborales extensas (superiores a 30 horas) merman críticamente la asistencia, disparando el indicador de "carga de estrés" y, consecuentemente, la deserción.
    3. **Hallazgo 3 (Impacto Económico):** Los estudiantes catalogados en el nivel socioeconómico "Bajo" presentan tasas de abandono proporcionalmente mayores, agravadas por el factor logístico de la distancia al campus.
    """)

with col4:
    st.info("💡 Recomendaciones Organizacionales")
    st.markdown("""
    1. **Recomendación 1:** Desplegar de forma inmediata el modelo predictivo (Random Forest) en el sistema de matrícula para identificar perfiles en riesgo desde la primera semana de clases.
    2. **Recomendación 2:** Diseñar esquemas de horarios flexibles y "modalidades híbridas" (virtual/presencial) para estudiantes que acrediten jornadas laborales de tiempo completo.
    3. **Recomendación 3:** Gestionar convenios de apoyo económico (becas parciales o subsidios de transporte) dirigidos a los segmentos de mayor vulnerabilidad económica que habitan en zonas alejadas.
    """)
