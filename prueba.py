import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Analítico Universitario",
    page_icon="🎓",
    layout="wide"
)

# Título principal
st.title("🎓 Dashboard Analítico Universitario")
st.markdown("### Análisis de Datos de Admisiones, Matrícula y Retención Estudiantil")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('university_student_data.csv')
    return df

df = load_data()

# Sidebar con filtros mejorados
st.sidebar.header("🔍 Panel de Filtros")
st.sidebar.markdown("Selecciona los criterios para filtrar los datos:")

# Filtro de rango de años con slider
years = sorted(df['Year'].unique())
year_range = st.sidebar.select_slider(
    "📅 Rango de Años",
    options=years,
    value=(years[0], years[-1])
)

# Filtro de término con radio buttons
st.sidebar.markdown("**📚 Período Académico**")
term_option = st.sidebar.radio(
    "Selecciona el período:",
    ["Todos", "Spring (Primavera)", "Fall (Otoño)"],
    index=0
)

# Filtro de departamento
st.sidebar.markdown("**🏢 Departamento**")
dept_option = st.sidebar.selectbox(
    "Selecciona el departamento:",
    ["Todos los Departamentos", "Ingeniería", "Negocios", "Artes", "Ciencias"]
)

# Aplicar filtros
df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

if term_option == "Spring (Primavera)":
    df_filtered = df_filtered[df_filtered['Term'] == 'Spring']
elif term_option == "Fall (Otoño)":
    df_filtered = df_filtered[df_filtered['Term'] == 'Fall']

# Información sobre los filtros aplicados
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Datos Filtrados:**")
st.sidebar.info(f"**{len(df_filtered)}** registros seleccionados de **{len(df)}** totales")

# Verificar si hay datos
if df_filtered.empty:
    st.warning("⚠️ No hay datos disponibles para los filtros seleccionados. Por favor, ajusta tu selección.")
    st.stop()

# KPIs principales
st.markdown("## 📈 Indicadores Clave de Desempeño (KPIs)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_retention = df_filtered['Retention Rate (%)'].mean()
    retention_change = avg_retention - df['Retention Rate (%)'].mean()
    st.metric(
        label="📊 Tasa de Retención Promedio",
        value=f"{avg_retention:.1f}%",
        delta=f"{retention_change:.1f}%"
    )
    st.caption("Porcentaje de estudiantes que continúan sus estudios")

with col2:
    avg_satisfaction = df_filtered['Student Satisfaction (%)'].mean()
    satisfaction_change = avg_satisfaction - df['Student Satisfaction (%)'].mean()
    st.metric(
        label="😊 Satisfacción Estudiantil",
        value=f"{avg_satisfaction:.1f}%",
        delta=f"{satisfaction_change:.1f}%"
    )
    st.caption("Nivel de satisfacción reportado por estudiantes")

with col3:
    total_enrolled = df_filtered['Enrolled'].sum()
    enrolled_change = total_enrolled - df['Enrolled'].sum()
    st.metric(
        label="👥 Total Matriculados",
        value=f"{total_enrolled:,}",
        delta=f"{enrolled_change:,}"
    )
    st.caption("Número total de estudiantes matriculados")

with col4:
    avg_admission_rate = (df_filtered['Admitted'].sum() / df_filtered['Applications'].sum() * 100)
    st.metric(
        label="✅ Tasa de Admisión",
        value=f"{avg_admission_rate:.1f}%"
    )
    st.caption("Porcentaje de aplicantes admitidos")

st.markdown("---")

# Interpretación de KPIs
with st.expander("📖 Interpretación de los Indicadores", expanded=False):
    st.markdown("""
    **Tasa de Retención**: Mide el porcentaje de estudiantes que continúan matriculados año tras año. 
    Una tasa alta (>85%) indica satisfacción estudiantil y buena calidad académica.
    
    **Satisfacción Estudiantil**: Refleja la percepción general de los estudiantes sobre su experiencia 
    universitaria. Valores superiores al 80% son considerados excelentes.
    
    **Total Matriculados**: Indica el tamaño de la población estudiantil activa y es clave para 
    la planificación de recursos institucionales.
    
    **Tasa de Admisión**: Muestra el nivel de selectividad de la universidad. Una tasa más baja 
    puede indicar mayor competitividad y prestigio.
    """)

# Gráficos principales
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendencias Temporales", "🆚 Comparación de Períodos", "🏢 Análisis por Departamento", "📊 Vista General"])

with tab1:
    st.header("📈 Evolución Temporal de Indicadores Clave")
    
    # Agrupar por año para tendencias
    df_yearly = df_filtered.groupby('Year').agg({
        'Retention Rate (%)': 'mean',
        'Student Satisfaction (%)': 'mean',
        'Enrolled': 'sum',
        'Applications': 'sum',
        'Admitted': 'sum'
    }).reset_index()
    
    # Gráfico de líneas doble
    st.subheader("🎯 Retención y Satisfacción a lo Largo del Tiempo")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=df_yearly['Year'], y=df_yearly['Retention Rate (%)'], 
                   name="Tasa de Retención", mode='lines+markers',
                   line=dict(color='#2E86AB', width=3),
                   marker=dict(size=8)),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=df_yearly['Year'], y=df_yearly['Student Satisfaction (%)'], 
                   name="Satisfacción Estudiantil", mode='lines+markers',
                   line=dict(color='#A23B72', width=3),
                   marker=dict(size=8)),
        secondary_y=False
    )
    
    fig.update_xaxes(title_text="Año")
    fig.update_yaxes(title_text="Porcentaje (%)", secondary_y=False)
    fig.update_layout(height=450, hovermode='x unified', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interpretación
    st.markdown("""
    **💡 Interpretación:** Este gráfico muestra la evolución de dos métricas fundamentales:
    - La **tasa de retención** indica qué tan bien la universidad mantiene a sus estudiantes matriculados.
    - La **satisfacción estudiantil** refleja la calidad de la experiencia universitaria.
    
    Ambas métricas muestran una **tendencia positiva** durante el período analizado, lo que sugiere 
    mejoras continuas en la calidad académica y servicios estudiantiles.
    """)
    
    st.markdown("---")
    
    # Gráfico de enrollment
    st.subheader("👥 Evolución de la Matrícula Estudiantil")
    fig2 = px.area(df_yearly, x='Year', y='Enrolled', 
                   title='Total de Estudiantes Matriculados por Año')
    fig2.update_traces(line_color='#F18F01', fillcolor='rgba(241, 143, 1, 0.3)')
    fig2.update_layout(height=400)
    fig2.update_xaxes(title_text="Año")
    fig2.update_yaxes(title_text="Número de Estudiantes")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    **💡 Interpretación:** El gráfico de matrícula muestra un **crecimiento sostenido** en el número 
    de estudiantes inscritos. Este crecimiento es indicativo de la reputación creciente de la universidad 
    y su capacidad para atraer nuevos estudiantes.
    """)
    
    # Análisis de aplicaciones vs admitidos
    st.subheader("📝 Embudo de Admisión")
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_yearly['Year'], y=df_yearly['Applications'], 
                                  name='Aplicaciones', mode='lines+markers',
                                  line=dict(color='#06A77D', width=2)))
        fig3.add_trace(go.Scatter(x=df_yearly['Year'], y=df_yearly['Admitted'], 
                                  name='Admitidos', mode='lines+markers',
                                  line=dict(color='#D62839', width=2)))
        fig3.add_trace(go.Scatter(x=df_yearly['Year'], y=df_yearly['Enrolled'], 
                                  name='Matriculados', mode='lines+markers',
                                  line=dict(color='#F77F00', width=2)))
        fig3.update_layout(title='Aplicaciones → Admisiones → Matrícula', height=400)
        fig3.update_xaxes(title_text="Año")
        fig3.update_yaxes(title_text="Número de Estudiantes")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Análisis del Embudo")
        st.markdown("""
        Este gráfico representa el **proceso de admisión completo**:
        
        1. **Aplicaciones** (verde): Estudiantes interesados que aplican
        2. **Admitidos** (rojo): Estudiantes que cumplen requisitos
        3. **Matriculados** (naranja): Estudiantes que finalmente se inscriben
        
        **Hallazgos clave:**
        - Crecimiento constante en aplicaciones
        - Tasa de conversión estable
        - Capacidad institucional bien gestionada
        """)

with tab2:
    st.header("🆚 Comparación entre Períodos Académicos")
    st.markdown("Análisis comparativo entre los períodos de **Spring (Primavera)** y **Fall (Otoño)**")
    
    # Comparación por término
    df_term = df_filtered.groupby('Term').agg({
        'Retention Rate (%)': 'mean',
        'Student Satisfaction (%)': 'mean',
        'Enrolled': 'sum',
        'Applications': 'sum',
        'Admitted': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Métricas de Calidad por Período")
        fig3 = go.Figure(data=[
            go.Bar(name='Tasa de Retención', x=df_term['Term'], 
                   y=df_term['Retention Rate (%)'], marker_color='#2E86AB'),
            go.Bar(name='Satisfacción', x=df_term['Term'], 
                   y=df_term['Student Satisfaction (%)'], marker_color='#A23B72')
        ])
        fig3.update_layout(barmode='group', height=400)
        fig3.update_xaxes(title_text="Período")
        fig3.update_yaxes(title_text="Porcentaje (%)")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("🎓 Distribución de Matrícula")
        fig4 = px.pie(df_term, values='Enrolled', names='Term', 
                      title='Proporción de Estudiantes por Período',
                      hole=0.4, color_discrete_sequence=['#06A77D', '#F77F00'])
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Interpretación
    st.markdown("---")
    st.markdown("### 💡 Análisis Comparativo")
    
    if len(df_term) > 1:
        spring_data = df_term[df_term['Term'] == 'Spring'].iloc[0] if 'Spring' in df_term['Term'].values else None
        fall_data = df_term[df_term['Term'] == 'Fall'].iloc[0] if 'Fall' in df_term['Term'].values else None
        
        if spring_data is not None and fall_data is not None:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Spring - Retención", f"{spring_data['Retention Rate (%)']:.1f}%")
            with col2:
                st.metric("Fall - Retención", f"{fall_data['Retention Rate (%)']:.1f}%")
            with col3:
                diff = fall_data['Retention Rate (%)'] - spring_data['Retention Rate (%)']
                st.metric("Diferencia", f"{diff:.1f}%")
            
            st.markdown("""
            **Observaciones:**
            - Los períodos Spring y Fall muestran **patrones muy similares** en retención y satisfacción
            - La **distribución de matrícula** es equilibrada entre ambos períodos
            - Esta consistencia indica **estabilidad institucional** y procesos bien establecidos
            """)
    else:
        st.info("Selecciona 'Todos' los períodos en el filtro para ver la comparación completa.")

with tab3:
    st.header("🏢 Análisis de Matrícula por Departamento")
    
    # Preparar datos por departamento
    dept_data = pd.DataFrame({
        'Departamento': ['Ingeniería', 'Negocios', 'Artes', 'Ciencias'],
        'Total Matriculados': [
            df_filtered['Engineering Enrolled'].sum(),
            df_filtered['Business Enrolled'].sum(),
            df_filtered['Arts Enrolled'].sum(),
            df_filtered['Science Enrolled'].sum()
        ]
    })
    
    # Calcular porcentajes
    dept_data['Porcentaje'] = (dept_data['Total Matriculados'] / dept_data['Total Matriculados'].sum() * 100).round(1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Matrícula Total por Departamento")
        fig5 = px.bar(dept_data, x='Departamento', y='Total Matriculados',
                      title='Distribución de Estudiantes',
                      color='Total Matriculados',
                      color_continuous_scale='Viridis',
                      text='Total Matriculados')
        fig5.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig5.update_layout(height=400)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Proporción por Departamento")
        fig6 = px.pie(dept_data, values='Total Matriculados', names='Departamento',
                      title='Distribución Porcentual',
                      hole=0.4,
                      color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01', '#06A77D'])
        fig6.update_traces(textposition='inside', textinfo='percent+label')
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)
    
    # Tabla de datos
    st.subheader("📋 Tabla Resumen por Departamento")
    dept_data_display = dept_data.copy()
    dept_data_display['Porcentaje'] = dept_data_display['Porcentaje'].astype(str) + '%'
    st.dataframe(dept_data_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Tendencias por departamento
    st.subheader("📈 Evolución de Matrícula por Departamento")
    df_dept_trend = df_filtered.groupby('Year').agg({
        'Engineering Enrolled': 'sum',
        'Business Enrolled': 'sum',
        'Arts Enrolled': 'sum',
        'Science Enrolled': 'sum'
    }).reset_index()
    
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Engineering Enrolled'], 
                              name='Ingeniería', mode='lines+markers', line=dict(width=3)))
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Business Enrolled'], 
                              name='Negocios', mode='lines+markers', line=dict(width=3)))
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Arts Enrolled'], 
                              name='Artes', mode='lines+markers', line=dict(width=3)))
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Science Enrolled'], 
                              name='Ciencias', mode='lines+markers', line=dict(width=3)))
    fig7.update_layout(height=450, hovermode='x unified')
    fig7.update_xaxes(title_text="Año")
    fig7.update_yaxes(title_text="Número de Estudiantes")
    st.plotly_chart(fig7, use_container_width=True)
    
    # Interpretación por departamento
    st.markdown("### 💡 Análisis por Departamento")
    
    # Encontrar el departamento más grande
    max_dept = dept_data.loc[dept_data['Total Matriculados'].idxmax()]
    min_dept = dept_data.loc[dept_data['Total Matriculados'].idxmin()]
    
    st.markdown(f"""
    **Hallazgos Principales:**
    
    - **{max_dept['Departamento']}** lidera con **{max_dept['Total Matriculados']:,}** estudiantes ({max_dept['Porcentaje']}%)
    - **{min_dept['Departamento']}** tiene la menor matrícula con **{min_dept['Total Matriculados']:,}** estudiantes ({min_dept['Porcentaje']}%)
    - Todos los departamentos muestran **tendencias de crecimiento** positivas
    - La diversificación departamental indica una **oferta académica equilibrada**
    
    **Recomendación:** Considerar invertir más recursos en los departamentos de mayor demanda 
    mientras se fortalecen programas de menor matrícula para mantener la diversidad académica.
    """)

with tab4:
    st.header("📊 Vista General y Resumen Ejecutivo")
    
    # Estadísticas generales
    st.subheader("📈 Estadísticas Resumidas del Período Seleccionado")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📝 Aplicaciones")
        total_apps = df_filtered['Applications'].sum()
        st.metric("Total de Aplicaciones", f"{total_apps:,}")
        st.caption(f"Promedio por registro: {df_filtered['Applications'].mean():.0f}")
    
    with col2:
        st.markdown("### ✅ Admitidos")
        total_admitted = df_filtered['Admitted'].sum()
        admission_rate = (total_admitted / total_apps * 100) if total_apps > 0 else 0
        st.metric("Total Admitidos", f"{total_admitted:,}")
        st.caption(f"Tasa de admisión: {admission_rate:.1f}%")
    
    with col3:
        st.markdown("### 🎓 Matriculados")
        total_enrolled = df_filtered['Enrolled'].sum()
        yield_rate = (total_enrolled / total_admitted * 100) if total_admitted > 0 else 0
        st.metric("Total Matriculados", f"{total_enrolled:,}")
        st.caption(f"Tasa de rendimiento: {yield_rate:.1f}%")
    
    st.markdown("---")
    
    # Embudo visual
    st.subheader("🎯 Embudo de Conversión del Proceso de Admisión")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        funnel_data = pd.DataFrame({
            'Etapa': ['Aplicaciones Recibidas', 'Estudiantes Admitidos', 'Estudiantes Matriculados'],
            'Cantidad': [
                df_filtered['Applications'].sum(),
                df_filtered['Admitted'].sum(),
                df_filtered['Enrolled'].sum()
            ]
        })
        fig8 = px.funnel(funnel_data, x='Cantidad', y='Etapa', 
                         title='Del Interés a la Matrícula',
                         color='Etapa',
                         color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01'])
        fig8.update_layout(height=400)
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Tasas de Conversión")
        st.metric("Aplicaciones → Admisión", f"{admission_rate:.1f}%")
        st.metric("Admisión → Matrícula", f"{yield_rate:.1f}%")
        st.metric("Aplicaciones → Matrícula", f"{(total_enrolled/total_apps*100):.1f}%")
        
    st.markdown("---")
    
    # Resumen ejecutivo
    st.subheader("📋 Resumen Ejecutivo")
    
    st.markdown(f"""
    ### Análisis del Período {year_range[0]} - {year_range[1]}
    
    **Indicadores Generales:**
    - **Retención Promedio:** {df_filtered['Retention Rate (%)'].mean():.1f}% 
    - **Satisfacción Promedio:** {df_filtered['Student Satisfaction (%)'].mean():.1f}%
    - **Total de Estudiantes Matriculados:** {df_filtered['Enrolled'].sum():,}
    
    **Tendencias Observadas:**
    - {'📈 Crecimiento' if df_filtered.groupby('Year')['Enrolled'].sum().is_monotonic_increasing else '📉 Variación'} en la matrícula estudiantil
    - {'✅ Mejora continua' if df_filtered.groupby('Year')['Retention Rate (%)'].mean().is_monotonic_increasing else '⚠️ Fluctuación'} en tasas de retención
    - {'😊 Aumento sostenido' if df_filtered.groupby('Year')['Student Satisfaction (%)'].mean().is_monotonic_increasing else '⚡ Cambios'} en satisfacción estudiantil
    
    **Departamento Destacado:** {dept_data.loc[dept_data['Total Matriculados'].idxmax(), 'Departamento']} 
    con {dept_data['Total Matriculados'].max():,} estudiantes
    """)
    
    st.markdown("---")
    
    # Datos sin procesar
    st.subheader("🗂️ Datos Filtrados (Vista Detallada)")
    st.markdown(f"Mostrando **{len(df_filtered)}** registros basados en los filtros seleccionados:")
    st.dataframe(df_filtered, use_container_width=True, height=400)
    
    # Opción de descarga
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos filtrados como CSV",
        data=csv,
        file_name=f'datos_filtrados_{year_range[0]}_{year_range[1]}.csv',
        mime='text/csv',
    )

# Footer
st.markdown("---")
st.markdown("**Universidad de la Costa** | Curso de Minería de Datos | 2025")
st.markdown("*Dashboard creado para la Actividad 1 - Visualización de Datos y Despliegue de Dashboard*")
st.markdown("**Profesor:** José Escorcia-Gutierrez, Ph.D.")