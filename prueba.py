import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="University Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Título principal
st.title("🎓 University Student Analytics Dashboard")
st.markdown("### Data-Driven Insights for Admission and Retention")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('university_student_data.csv')
    return df

df = load_data()

# Sidebar con filtros
st.sidebar.header("📊 Filters")

# Filtro de año
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=years,
    default=years
)

# Filtro de término
terms = df['Term'].unique()
selected_terms = st.sidebar.multiselect(
    "Select Term(s)",
    options=terms,
    default=terms
)

# Filtrar datos
df_filtered = df[
    (df['Year'].isin(selected_years)) & 
    (df['Term'].isin(selected_terms))
]

# Verificar si hay datos
if df_filtered.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
    st.stop()

# KPIs principales
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_retention = df_filtered['Retention Rate (%)'].mean()
    st.metric(
        label="📈 Avg Retention Rate",
        value=f"{avg_retention:.1f}%",
        delta=f"{avg_retention - df['Retention Rate (%)'].mean():.1f}%"
    )

with col2:
    avg_satisfaction = df_filtered['Student Satisfaction (%)'].mean()
    st.metric(
        label="😊 Avg Student Satisfaction",
        value=f"{avg_satisfaction:.1f}%",
        delta=f"{avg_satisfaction - df['Student Satisfaction (%)'].mean():.1f}%"
    )

with col3:
    total_enrolled = df_filtered['Enrolled'].sum()
    st.metric(
        label="👥 Total Enrolled",
        value=f"{total_enrolled:,}",
        delta=f"{total_enrolled - df['Enrolled'].sum()}"
    )

with col4:
    avg_admission_rate = (df_filtered['Admitted'].sum() / df_filtered['Applications'].sum() * 100)
    st.metric(
        label="✅ Admission Rate",
        value=f"{avg_admission_rate:.1f}%"
    )

st.markdown("---")

# Gráficos principales
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends Over Time", "🆚 Term Comparison", "🏢 Department Analysis", "📊 Overview"])

with tab1:
    st.subheader("Retention Rate and Satisfaction Trends")
    
    # Agrupar por año para tendencias
    df_yearly = df_filtered.groupby('Year').agg({
        'Retention Rate (%)': 'mean',
        'Student Satisfaction (%)': 'mean',
        'Enrolled': 'sum'
    }).reset_index()
    
    # Gráfico de líneas doble
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=df_yearly['Year'], y=df_yearly['Retention Rate (%)'], 
                   name="Retention Rate", mode='lines+markers',
                   line=dict(color='#1f77b4', width=3)),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=df_yearly['Year'], y=df_yearly['Student Satisfaction (%)'], 
                   name="Student Satisfaction", mode='lines+markers',
                   line=dict(color='#ff7f0e', width=3)),
        secondary_y=False
    )
    
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Percentage (%)", secondary_y=False)
    fig.update_layout(height=400, hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de enrollment
    st.subheader("Enrollment Trends")
    fig2 = px.line(df_yearly, x='Year', y='Enrolled', 
                   markers=True, 
                   title='Total Enrollment by Year')
    fig2.update_traces(line_color='#2ca02c', line_width=3)
    fig2.update_layout(height=350)
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Spring vs Fall Term Comparison")
    
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
        fig3 = go.Figure(data=[
            go.Bar(name='Retention Rate', x=df_term['Term'], 
                   y=df_term['Retention Rate (%)'], marker_color='#1f77b4'),
            go.Bar(name='Satisfaction', x=df_term['Term'], 
                   y=df_term['Student Satisfaction (%)'], marker_color='#ff7f0e')
        ])
        fig3.update_layout(barmode='group', title='Retention vs Satisfaction by Term', height=350)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = px.pie(df_term, values='Enrolled', names='Term', 
                      title='Enrollment Distribution by Term',
                      hole=0.4, color_discrete_sequence=['#2ca02c', '#d62728'])
        fig4.update_layout(height=350)
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("Department Enrollment Analysis")
    
    # Preparar datos por departamento
    dept_data = pd.DataFrame({
        'Department': ['Engineering', 'Business', 'Arts', 'Science'],
        'Total Enrolled': [
            df_filtered['Engineering Enrolled'].sum(),
            df_filtered['Business Enrolled'].sum(),
            df_filtered['Arts Enrolled'].sum(),
            df_filtered['Science Enrolled'].sum()
        ]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig5 = px.bar(dept_data, x='Department', y='Total Enrolled',
                      title='Total Enrollment by Department',
                      color='Total Enrolled',
                      color_continuous_scale='Viridis')
        fig5.update_layout(height=350)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        fig6 = px.pie(dept_data, values='Total Enrolled', names='Department',
                      title='Department Distribution',
                      hole=0.4)
        fig6.update_layout(height=350)
        st.plotly_chart(fig6, use_container_width=True)
    
    # Tendencias por departamento
    st.subheader("Department Enrollment Trends Over Time")
    df_dept_trend = df_filtered.groupby('Year').agg({
        'Engineering Enrolled': 'sum',
        'Business Enrolled': 'sum',
        'Arts Enrolled': 'sum',
        'Science Enrolled': 'sum'
    }).reset_index()
    
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Engineering Enrolled'], 
                              name='Engineering', mode='lines+markers'))
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Business Enrolled'], 
                              name='Business', mode='lines+markers'))
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Arts Enrolled'], 
                              name='Arts', mode='lines+markers'))
    fig7.add_trace(go.Scatter(x=df_dept_trend['Year'], y=df_dept_trend['Science Enrolled'], 
                              name='Science', mode='lines+markers'))
    fig7.update_layout(title='Enrollment Trends by Department', height=400, hovermode='x unified')
    st.plotly_chart(fig7, use_container_width=True)

with tab4:
    st.subheader("Complete Overview")
    
    # Tabla resumen
    st.markdown("#### Summary Statistics")
    summary_stats = df_filtered.agg({
        'Applications': 'sum',
        'Admitted': 'sum',
        'Enrolled': 'sum',
        'Retention Rate (%)': 'mean',
        'Student Satisfaction (%)': 'mean'
    }).round(2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(summary_stats, use_container_width=True)
    
    with col2:
        # Funnel chart
        funnel_data = pd.DataFrame({
            'Stage': ['Applications', 'Admitted', 'Enrolled'],
            'Count': [
                df_filtered['Applications'].sum(),
                df_filtered['Admitted'].sum(),
                df_filtered['Enrolled'].sum()
            ]
        })
        fig8 = px.funnel(funnel_data, x='Count', y='Stage', 
                         title='Admission Funnel')
        fig8.update_layout(height=350)
        st.plotly_chart(fig8, use_container_width=True)
    
    # Datos sin procesar
    st.markdown("#### Filtered Data")
    st.dataframe(df_filtered, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Universidad de la Costa** | Data Mining Course | 2025")
st.markdown("*Dashboard created for Activity 1 - Data Visualization*")