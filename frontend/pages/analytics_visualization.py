# Analytics & Visualization page implementationimport streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
from components.charts import (
    productivity_chart, 
    task_allocation_heatmap, 
    network_analysis_chart,
    comparative_chart
)

def show_analytics_visualization():
    st.header("Analytics & Visualization")
    
    # Verificar si hay resultados de simulación
    if 'simulation_results' not in st.session_state or st.session_state.simulation_results is None:
        st.warning("No simulation results available. Please run a simulation first.")
        return
    
    # Extraer resultados
    results = st.session_state.simulation_results
    results_df = results["results_df"]
    
    # Crear pestañas para diferentes visualizaciones
    tabs = st.tabs([
        "Productivity Evolution", 
        "Task Allocation", 
        "Network Analysis", 
        "Comparative Analysis"
    ])
    
    # Pestaña 1: Evolución de Productividad
    with tabs[0]:
        st.subheader("Productivity Evolution")
        
        # Controles de filtro
        metric_col, filter_col = st.columns([2, 1])
        
        with metric_col:
            selected_metric = st.selectbox(
                "Select Metric",
                ["productivity", "cost_efficiency", "innovation_rate", "agent_satisfaction"],
                index=0,
                format_func=lambda x: x.replace("_", " ").title()
            )
        
        with filter_col:
            show_trendline = st.checkbox("Show Trendline", value=True)
            show_confidence = st.checkbox("Show Confidence Interval", value=True)
        
        # Generar datos de serie temporal para la métrica seleccionada
        # (Simulamos datos para varias iteraciones y períodos)
        time_periods = 20
        iterations = len(results_df)
        
        time_data = []
        for iter_idx in range(iterations):
            base_value = results_df.iloc[iter_idx][selected_metric]
            for period in range(time_periods):
                # Simular cambio con tendencia
                value = base_value * (1 + 0.02 * period) + np.random.normal(0, 0.05)
                time_data.append({
                    "iteration": iter_idx + 1,
                    "period": period + 1,
                    "value": value
                })
        
        time_df = pd.DataFrame(time_data)
        
        # Mostrar gráfico
        productivity_chart(time_df, selected_metric, show_trendline, show_confidence)
    
    # Pestaña 2: Mapa de Calor de Asignación de Tareas
    with tabs[1]:
        st.subheader("Task Allocation Analysis")
        
        # Controles
        col1, col2 = st.columns(2)
        with col1:
            allocation_view = st.selectbox(
                "View By",
                ["Agent Type", "Task Type", "Time Period"],
                index=0
            )
        
        with col2:
            normalized = st.checkbox("Normalize Values", value=True)
        
        # Generar datos simulados para el mapa de calor
        # (Dependiendo de la vista seleccionada, creamos diferentes datos)
        if allocation_view == "Agent Type":
            agent_types = ["Manager", "Senior Worker", "Junior Worker", "Innovator", "Specialist"]
            task_types = ["Decision", "Execution", "Analysis", "Innovation", "Support"]
            
            # Crear matriz de asignación
            data = np.random.uniform(0, 1, size=(len(agent_types), len(task_types)))
            if normalized:
                data = data / data.sum(axis=1, keepdims=True)
            
            # Crear DataFrame
            heatmap_df = pd.DataFrame(data, index=agent_types, columns=task_types)
        
        elif allocation_view == "Task Type":
            task_types = ["Decision", "Execution", "Analysis", "Innovation", "Support"]
            time_periods = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]
            
            # Crear matriz de asignación
            data = np.random.uniform(0, 1, size=(len(task_types), len(time_periods)))
            if normalized:
                data = data / data.sum(axis=0, keepdims=True)
            
            # Crear DataFrame
            heatmap_df = pd.DataFrame(data, index=task_types, columns=time_periods)
        
        else:  # Time Period
            time_periods = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]
            metrics = ["Efficiency", "Quality", "Time to Complete", "Resource Usage", "Innovation Impact"]
            
            # Crear matriz de asignación
            data = np.random.uniform(0, 1, size=(len(time_periods), len(metrics)))
            
            # Crear DataFrame
            heatmap_df = pd.DataFrame(data, index=time_periods, columns=metrics)
        
        # Mostrar mapa de calor
        task_allocation_heatmap(heatmap_df, allocation_view, normalized)
    
    # Pestaña 3: Análisis de Red
    with tabs[2]:
        st.subheader("Organizational Network Analysis")
        
        # Controles
        col1, col2 = st.columns(2)
        with col1:
            network_metric = st.selectbox(
                "Network Metric",
                ["Communication Frequency", "Knowledge Transfer", "Task Delegation", "Decision Influence"],
                index=0
            )
        
        with col2:
            threshold = st.slider(
                "Connection Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.05,
                help="Minimum value for connections to be displayed"
            )
        
        # Mostrar gráfico de red
        network_analysis_chart(network_metric, threshold)
    
    # Pestaña 4: Análisis Comparativo
    with tabs[3]:
        st.subheader("Comparative Analysis")
        
        # Controles
        col1, col2 = st.columns(2)
        with col1:
            x_metric = st.selectbox(
                "X-Axis Metric",
                ["productivity", "cost_efficiency", "innovation_rate", "agent_satisfaction"],
                index=0,
                format_func=lambda x: x.replace("_", " ").title()
            )
        
        with col2:
            y_metric = st.selectbox(
                "Y-Axis Metric",
                ["productivity", "cost_efficiency", "innovation_rate", "agent_satisfaction"],
                index=1,
                format_func=lambda x: x.replace("_", " ").title()
            )
        
        color_metric = st.selectbox(
            "Color By",
            ["iteration", "duration_seconds"],
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        # Mostrar gráfico comparativo
        comparative_chart(results_df, x_metric, y_metric, color_metric)
    
    # Sección de descarga de datos
    st.markdown("---")
    st.subheader("Download Analysis Data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download Raw Results (CSV)",
            data=results_df.to_csv(index=False),
            file_name="agentflow_results.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="Download Simulation Log (TXT)",
            data="\n".join(results["logs"]),
            file_name="agentflow_simulation_log.txt",
            mime="text/plain"
        )