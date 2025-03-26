import streamlit as st
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import random

def display_organization_graph(hierarchy_depth=3, span_of_control=5, centralization=0.5, 
                               vertical_comm=0.7, horizontal_comm=0.4):
    """
    Muestra un gráfico interactivo de la estructura organizacional.
    
    Args:
        hierarchy_depth: Número de niveles jerárquicos
        span_of_control: Número promedio de subordinados por manager
        centralization: Nivel de centralización (0-1)
        vertical_comm: Intensidad de comunicación vertical (0-1)
        horizontal_comm: Intensidad de comunicación horizontal (0-1)
    """
    # Crear grafo direccionado
    G = nx.DiGraph()
    
    # Añadir nodos y edges basados en los parámetros
    node_id = 0
    managers_by_level = {0: [0]}  # Nivel 0 es el CEO
    
    # Añadir nodo raíz (CEO)
    G.add_node(node_id, role="CEO", level=0)
    node_id += 1
    
    # Crear estructura jerárquica
    for level in range(1, hierarchy_depth):
        managers_by_level[level] = []
        
        # Número de managers en este nivel
        if level == hierarchy_depth - 1:
            # El último nivel son trabajadores
            role = "Worker"
        elif level == 1:
            # Ejecutivos de alto nivel
            role = "Executive"
        else:
            # Managers intermedios
            role = "Manager"
        
        # Para cada manager del nivel anterior
        for parent_id in managers_by_level[level - 1]:
            # Determinar número de subordinados (con algo de variación)
            num_subordinates = max(1, int(span_of_control + random.randint(-1, 1)))
            
            # Crear nodos de subordinados
            for _ in range(num_subordinates):
                G.add_node(node_id, role=role, level=level)
                G.add_edge(parent_id, node_id, type="hierarchical")
                managers_by_level[level].append(node_id)
                node_id += 1
    
    # Añadir conexiones horizontales (entre pares) basadas en horizontal_comm
    for level in range(1, hierarchy_depth):
        managers = managers_by_level[level]
        
        # Ajustar probabilidad de conexión basada en horizontal_comm
        conn_probability = horizontal_comm * 0.3  # Escalar para no tener demasiadas conexiones
        
        for i in range(len(managers)):
            for j in range(i+1, len(managers)):
                # Añadir conexión con cierta probabilidad
                if random.random() < conn_probability:
                    # Conexión bidireccional entre pares
                    G.add_edge(managers[i], managers[j], type="horizontal")
                    G.add_edge(managers[j], managers[i], type="horizontal")
    
    # Añadir innovadores (si centralization es baja, más innovadores conectados directamente a ejecutivos)
    num_innovators = max(1, int((1 - centralization) * 5) + 1)
    innovator_level = min(2, hierarchy_depth - 1)  # Nivel al que se conectan principalmente
    
    for i in range(num_innovators):
        G.add_node(node_id, role="Innovator", level=innovator_level)
        
        # Conectar a managers basado en centralización
        if random.random() < centralization:
            # Conexión a CEO o ejecutivos (centralizado)
            parent_idx = random.randint(0, len(managers_by_level[1]) - 1)
            parent_id = managers_by_level[1][parent_idx]
        else:
            # Conexión a managers intermedios (descentralizado)
            level = min(2, hierarchy_depth - 1)
            parent_idx = random.randint(0, len(managers_by_level[level]) - 1)
            parent_id = managers_by_level[level][parent_idx]
        
        G.add_edge(parent_id, node_id, type="innovation")
        G.add_edge(node_id, parent_id, type="innovation")
        
        node_id += 1
    
    # Preparar datos para visualización
    pos = hierarchy_pos(G)
    
    # Convertir posiciones a coordenadas x, y
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    # Preparar colores de nodos según rol
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        role = G.nodes[node]["role"]
        if role == "CEO":
            node_colors.append("rgba(255, 0, 0, 0.8)")  # Rojo
            node_sizes.append(20)
        elif role == "Executive":
            node_colors.append("rgba(255, 165, 0, 0.8)")  # Naranja
            node_sizes.append(15)
        elif role == "Manager":
            node_colors.append("rgba(0, 0, 255, 0.8)")  # Azul
            node_sizes.append(12)
        elif role == "Worker":
            node_colors.append("rgba(0, 128, 0, 0.8)")  # Verde
            node_sizes.append(8)
        elif role == "Innovator":
            node_colors.append("rgba(128, 0, 128, 0.8)")  # Púrpura
            node_sizes.append(10)
    
    # Crear líneas para edges
    edge_x = []
    edge_y = []
    edge_colors = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        # Añadir línea segmentada
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Colorear según tipo de conexión
        if G.edges[edge]["type"] == "hierarchical":
            edge_colors.append("rgba(100, 100, 100, 0.6)")
        elif G.edges[edge]["type"] == "horizontal":
            edge_colors.append("rgba(0, 200, 200, 0.4)")
        elif G.edges[edge]["type"] == "innovation":
            edge_colors.append("rgba(200, 0, 200, 0.5)")
    
    # Crear figura de Plotly
    fig = go.Figure()
    
    # Añadir edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color=edge_colors),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Añadir nodos
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_sizes,
            line=dict(width=1, color='rgba(50, 50, 50, 0.8)')
        ),
        hovertemplate='%{text}<extra></extra>',
        text=[G.nodes[node]["role"] + f" (Level {G.nodes[node]['level']})" for node in G.nodes()]
    ))
    
    # Personalizar diseño
    fig.update_layout(
        title="Organizational Structure",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        template="plotly_white"
    )
    
    # Mostrar figura
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar leyenda
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 CEO")
        st.markdown("🟠 Executive")
    with col2:
        st.markdown("🔵 Manager")
        st.markdown("🟢 Worker")
    with col3:
        st.markdown("🟣 Innovator")

def hierarchy_pos(G, root=0, width=1., height=1.):
    """
    Posiciona los nodos en un layout jerárquico.
    Adaptado de: https://stackoverflow.com/a/29597209/2966723
    """
    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5,
                      pos=None, parent=None, level_width=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
            
        children = list(G.neighbors(root))
        if parent is not None:
            children.remove(parent)
            
        if len(children) != 0:
            if level_width is None:
                level_width = {0: 1}
                
            this_level = G.nodes[root]['level']
            next_level = this_level + 1
            
            if next_level not in level_width:
                level_width[next_level] = 0
                
            level_width[next_level] += len(children)
            
            dx = width / level_width[next_level]
            nextx = xcenter - width/2 - dx/2
            
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                    vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent=root, level_width=level_width)
        return pos
            
    return _hierarchy_pos(G, root, width, height)