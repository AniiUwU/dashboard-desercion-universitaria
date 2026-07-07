import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard: Deserción Universitaria", page_icon="🐱", layout="wide")
st.title("🎓 Análisis de Deserción Universitaria")
st.markdown("Dashboard interactivo para la toma de decisiones académicas en la sede Lima Norte.")

# Cargar los datos
@st.cache_data
def cargar_datos():
    return pd.read_csv('dataset_personal.csv')

df_original = cargar_datos()

# ==========================================
# MENÚ LATERAL INTERACTIVO (SIDEBAR)
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
st.sidebar.info("🐱 Proyecto de Inteligencia de Negocios y Big Data.")

# ==========================================
# SISTEMA DE PESTAÑAS (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 Panel Principal", "🔥 Mapa de Calor", "📁 Base de Datos"])

with tab1:
    st.header("Indicadores Generales")
    tasa_desercion = (df['desercion'].mean() * 100).round(2)
    st.metric(label="Tasa Histórica de Deserción (Filtrada)", value=f"{tasa_desercion}%", delta="Riesgo Moderado", delta_color="inverse")

    # Fila 1
    col1, col2 = st.columns(2)
    with col1:
        df_agrupado = df.groupby('nivel_socioeconomico')['desercion'].mean().reset_index()
        df_agrupado['desercion'] = df_agrupado['desercion'] * 100
        fig_barras = px.bar(df_agrupado, x='nivel_socioeconomico', y='desercion', 
                            labels={'desercion': 'Tasa de Deserción (%)', 'nivel_socioeconomico': 'Nivel'},
                            color='nivel_socioeconomico', color_discrete_sequence=px.colors.qualitative.Pastel,
                            title="Deserción por Nivel Socioeconómico")
        st.plotly_chart(fig_barras, use_container_width=True)

    with col2:
        df_estado = df['desercion'].map({0: 'Continúa', 1: 'Desertó'}).value_counts().reset_index()
        df_estado.columns = ['Estado', 'Cantidad']
        fig_pie = px.pie(df_estado, values='Cantidad', names='Estado', hole=0.4,
                         color_discrete_sequence=['#FF99CC', '#99CCFF'],
                         title="Proporción del Estado Actual")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Fila 2
    col3, col4 = st.columns(2)
    with col3:
        fig_box = px.box(df, x='desercion', y='promedio_notas', 
                         labels={'desercion': 'Estado (0=Continúa, 1=Desertó)', 'promedio_notas': 'Promedio Académico'},
                         color='desercion', category_orders={"desercion": [0, 1]},
                         title="Promedio de Notas vs Deserción")
        st.plotly_chart(fig_box, use_container_width=True)

    with col4:
        fig_scatter = px.scatter(df, x='asistencia_pct', y='horas_trabajo_semanal', color='desercion', 
                                 size='carga_estres',
                                 labels={'asistencia_pct': 'Asistencia (%)', 'horas_trabajo_semanal': 'Horas de Trabajo'},
                                 title="Impacto del Trabajo y Asistencia")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.header("Análisis de Correlación")
    st.markdown("Este mapa de calor permite identificar qué variables numéricas tienen mayor relación directa con la deserción.")
    
    # Filtrar solo numéricas para el heatmap
    df_numerico = df.select_dtypes(include=['float64', 'int64', 'int32'])
    matriz_corr = df_numerico.corr()
    
    fig_heatmap = px.imshow(matriz_corr, text_auto=".2f", aspect="auto", 
                            color_continuous_scale="RdPu", 
                            title="Matriz de Correlaciones Numéricas")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab3:
    st.header("Explorador de Datos")
    st.markdown("Visualiza la data cruda generada por el proceso ETL o descárgala para análisis externo.")
    st.dataframe(df, use_container_width=True)
    
    # Botón de descarga
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar Dataset CSV",
        data=csv,
        file_name='dataset_filtrado.csv',
        mime='text/csv',
    )

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
