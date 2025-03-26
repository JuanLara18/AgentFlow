import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import random

def sample_scenario_chart(scenario_type):
    """
    Muestra un gráfico de ejemplo para previsualizar un escenario.
    
    Args:
        scenario_type: Tipo de escenario a visualizar
    """
    # Generar datos de ejemplo según el escenario
    if scenario_type == "classic_hierarchy":
        # Estructura clásica jerárquica
        x = list(range(5))
        productivity = [1.0, 1.2, 1.3, 1.35, 1.4]
        cost = [1.0, 1.1, 1.15, 1.25, 1.3]
        innovation = [1.0, 1.05, 1.1, 1.12, 1.15]
        title = "Classic Hierarchy - Expected Performance"
    
    elif scenario_type == "innovation_driven":
        # Estructura enfocada en innovación
        x = list(range(5))
        productivity = [1.0, 1.1, 1.25, 1.45, 1.7]
        cost = [1.0, 1.15, 1.3, 1.5, 1.7]
        innovation = [1.0, 1.15, 1.35, 1.6, 1.9]
        title = "Innovation-driven - Expected Performance"
    
    else:  # "decentralized"
        # Estructura descentralizada
        x = list(range(5))
        productivity = [1.0, 1.15, 1.35, 1.5, 1.6]
        cost = [1.0, 1.05, 1.1, 1.15, 1.2]
        innovation = [1.0, 1.1, 1.2, 1.3, 1.45]
        title = "Decentralized - Expected Performance"
    
    # Crear figura
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=productivity,
        mode='lines+markers',
        name='Productivity',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=cost,
        mode='lines+markers',
        name='Cost',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=innovation,
        mode='lines+markers',
        name='Innovation',
        line=dict(color='green', width=2)
    ))
    
    # Actualizar layout
    fig.update_layout(
        xaxis=dict(title="Time Periods", tickvals=x, ticktext=[f"T{i}" for i in x]),
        yaxis=dict(title="Relative Performance"),
        title=title,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_white"
    )
    
    # Mostrar figura
    st.plotly_chart(fig, use_container_width=True)

def productivity_chart(data_df, metric, show_trendline=True, show_confidence=True):
    """
    Muestra un gráfico de evolución de productividad.
    
    Args:
        data_df: DataFrame con los datos (debe tener columnas 'iteration', 'period', 'value')
        metric: Métrica a visualizar
        show_trendline: Si se muestra la línea de tendencia
        show_confidence: Si se muestra el intervalo de confianza
    """
    # Preparar datos promedio por período
    avg_df = data_df.groupby('period')['value'].agg(['mean', 'std']).reset_index()
    avg_df['upper'] = avg_df['mean'] + avg_df['std']
    avg_df['lower'] = avg_df['mean'] - avg_df['std']
    
    # Crear figura base
    fig = px.line(
        data_df, 
        x='period', 
        y='value', 
        color='iteration',
        labels={'period': 'Time Period', 'value': metric.replace('_', ' ').title()},
        title=f'Evolution of {metric.replace("_", " ").title()} Over Time'
    )
    
    # Añadir línea de tendencia
    if show_trendline:
        fig.add_trace(
            go.Scatter(
                x=avg_df['period'],
                y=avg_df['mean'],
                mode='lines',
                line=dict(color='black', width=3, dash='dash'),
                name='Average Trend'
            )
        )
    
    # Añadir intervalo de confianza
    if show_confidence:
        fig.add_trace(
            go.Scatter(
                x=avg_df['period'].tolist() + avg_df['period'].tolist()[::-1],
                y=avg_df['upper'].tolist() + avg_df['lower'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(0,0,0,0.1)',
                line=dict(color='rgba(0,0,0,0)'),
                hoverinfo='skip',
                showlegend=False
            )
        )
    
    # Actualizar layout
    fig.update_layout(
        xaxis=dict(title="Time Period"),
        yaxis=dict(title=metric.replace('_', ' ').title()),
        legend=dict(title="Iteration"),
        hovermode="x unified",
        template="plotly_white"
    )
    
    # Mostrar figura
    st.plotly_chart(fig, use_container_width=True)

def task_allocation_heatmap(data_df, view_type, normalized=True):
    """
    Muestra un mapa de calor para la asignación de tareas.
    
    Args:
        data_df: DataFrame con los datos para el mapa de calor
        view_type: Tipo de vista ('Agent Type', 'Task Type', 'Time Period')
        normalized: Si los datos están normalizados
    """
    # Crear figura
    fig = px.imshow(
        data_df,
        labels=dict(x="Columns", y="Rows", color="Value"),
        color_continuous_scale='Blues',
        aspect="auto"
    )
    
    # Ajustar título según la vista
    title = f"Task Allocation by {view_type}"
    if normalized:
        title += " (Normalized)"
    
    # Añadir texto de valores en las celdas
    for i in range(len(data_df.index)):
        for j in range(len(data_df.columns)):
            value = data_df.iloc[i, j]
            text_format = '.0%' if normalized else '.2f'
            fig.add_annotation(
                x=j, y=i,
                text=f"{value:{text_format}}",
                showarrow=False,
                font=dict(color="white" if value > 0.5 else "black")
            )
    
    # Actualizar layout
    fig.update_layout(
        title=title,
        margin=dict(l=40, r=40, t=40, b=20),
        coloraxis_colorbar=dict(title="Value"),
        template="plotly_white"
    )
    
    # Mostrar figura
    st.plotly_chart(fig, use_container_width=True)

def network_analysis_chart(metric_type, threshold=0.3):
    """
    Muestra un análisis de red organizacional.
    
    Args:
        metric_type: Tipo de métrica para la red
        threshold: Umbral para mostrar conexiones
    """
    # Crear grafo simulado
    G = nx.Graph()
    
    # Agregar nodos de diferentes tipos
    node_types = {
        "Manager": 5,
        "Worker": 15,
        "Innovator": 3
    }
    
    node_id = 0
    node_colors = []
    node_sizes = []
    node_labels = {}
    
    for node_type, count in node_types.items():
        for i in range(count):
            G.add_node(node_id, type=node_type)
            
            if node_type == "Manager":
                node_colors.append("rgba(255, 0, 0, 0.8)")
                node_sizes.append(15)
            elif node_type == "Worker":
                node_colors.append("rgba(0, 0, 255, 0.8)")
                node_sizes.append(10)
            else:  # Innovator
                node_colors.append("rgba(0, 255, 0, 0.8)")
                node_sizes.append(12)
            
            node_labels[node_id] = f"{node_type} {i+1}"
            node_id += 1
    
    # Añadir aristas con diferentes pesos
    # La densidad dependerá del tipo de métrica
    if metric_type == "Communication Frequency":
        edge_probability = 0.3
        max_weight = 1.0
    elif metric_type == "Knowledge Transfer":
        edge_probability = 0.2
        max_weight = 0.8
    elif metric_type == "Task Delegation":
        edge_probability = 0.15
        max_weight = 0.7
    else:  # Decision Influence
        edge_probability = 0.1
        max_weight = 0.6
    
    edge_weights = []
    
    for i in range(len(G.nodes)):
        for j in range(i+1, len(G.nodes)):
            if random.random() < edge_probability:
                weight = random.uniform(0.1, max_weight)
                if weight >= threshold:
                    G.add_edge(i, j, weight=weight)
                    edge_weights.append(weight)
    
    # Posicionamiento de nodos (force-directed)
    pos = nx.spring_layout(G, seed=42)
    
    # Preparar datos para Plotly
    edge_x = []
    edge_y = []
    edge_traces = []
    
    # Primero añadir todas las aristas con diferentes grosores
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = G.edges[edge]['weight']
        
        # Crear un trace separado para cada arista para poder tener diferentes grosores
        edge_trace = go.Scatter(
            x=[x0, x1, None], 
            y=[y0, y1, None],
            line=dict(width=weight*5, color=f'rgba(50, 50, 50, {weight})'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
        
        edge_traces.append(edge_trace)
    
    # Crear nodos
    node_x = []
    node_y = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    # Crear trace para los nodos
    node_trace = go.Scatter(
        x=node_x, 
        y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color=node_colors,
            size=node_sizes,
            line=dict(width=1, color='rgba(50, 50, 50, 0.8)')
        ),
        text=[node_labels[node] for node in G.nodes()],
        name='Nodes'
    )
    
    # Crear figura
    fig = go.Figure()
    
    # Añadir todos los traces de aristas
    for edge_trace in edge_traces:
        fig.add_trace(edge_trace)
    
    # Añadir nodos
    fig.add_trace(node_trace)
    
    # Actualizar layout
    fig.update_layout(
        title=f'Organizational Network: {metric_type} (Threshold: {threshold})',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=20, r=20, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template="plotly_white"
    )
    
    # Mostrar figura
    st.plotly_chart(fig, use_container_width=True)
    
    # Añadir leyenda manual
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 Manager")
    with col2:
        st.markdown("🔵 Worker")
    with col3:
        st.markdown("🟢 Innovator")
    
    # Añadir estadísticas de red
    st.markdown("### Network Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nodes", len(G.nodes()))
    with col2:
        st.metric("Connections", len(G.edges()))
    with col3:
        density = len(G.edges()) / (len(G.nodes()) * (len(G.nodes()) - 1) / 2)
        st.metric("Network Density", f"{density:.2f}")
        
def comparative_chart(data_df, x_metric, y_metric, color_metric):
    """
    Muestra un gráfico comparativo entre diferentes métricas.
    
    Args:
        data_df: DataFrame con los datos
        x_metric: Métrica para el eje X
        y_metric: Métrica para el eje Y
        color_metric: Métrica para el color
    """
    # Crear figura
    fig = px.scatter(
        data_df,
        x=x_metric,
        y=y_metric,
        color=color_metric,
        size=[15] * len(data_df),
        hover_data=data_df.columns,
        labels={
            x_metric: x_metric.replace('_', ' ').title(),
            y_metric: y_metric.replace('_', ' ').title(),
            color_metric: color_metric.replace('_', ' ').title()
        },
        title=f"{y_metric.replace('_', ' ').title()} vs. {x_metric.replace('_', ' ').title()} by {color_metric.replace('_', ' ').title()}"
    )
    
    # Añadir línea de tendencia
    fig.add_trace(
        go.Scatter(
            x=data_df[x_metric],
            y=data_df[y_metric].rolling(window=3, min_periods=1).mean(),
            mode='lines',
            line=dict(color='rgba(0,0,0,0.5)', width=2, dash='dash'),
            name='Trend'
        )
    )
    
    # Actualizar layout
    fig.update_layout(
        xaxis=dict(title=x_metric.replace('_', ' ').title()),
        yaxis=dict(title=y_metric.replace('_', ' ').title()),
        coloraxis_colorbar=dict(title=color_metric.replace('_', ' ').title()),
        template="plotly_white",
        height=500
    )
    
    # Mostrar figura
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar correlación
    correlation = data_df[x_metric].corr(data_df[y_metric])
    st.info(f"Correlation between {x_metric.replace('_', ' ').title()} and {y_metric.replace('_', ' ').title()}: {correlation:.2f}")
    
    # Añadir resumen de estadísticas
    st.subheader("Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{x_metric.replace('_', ' ').title()}**")
        st.metric("Mean", f"{data_df[x_metric].mean():.2f}")
        st.metric("Min", f"{data_df[x_metric].min():.2f}")
        st.metric("Max", f"{data_df[x_metric].max():.2f}")
    
    with col2:
        st.markdown(f"**{y_metric.replace('_', ' ').title()}**")
        st.metric("Mean", f"{data_df[y_metric].mean():.2f}")
        st.metric("Min", f"{data_df[y_metric].min():.2f}")
        st.metric("Max", f"{data_df[y_metric].max():.2f}")