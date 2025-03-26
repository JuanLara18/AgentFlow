import os
import json
import random
import pandas as pd
import networkx as nx
from datetime import datetime

def save_simulation_results(results, simulation_id, path=None):
    """
    Guarda los resultados de una simulación.
    
    Args:
        results: Diccionario con resultados de la simulación
        simulation_id: ID único de la simulación
        path: Ruta donde guardar los resultados (opcional)
    
    Returns:
        Ruta del archivo guardado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if path is None:
        # Usar directorio por defecto
        results_dir = os.path.join("data", "results")
        os.makedirs(results_dir, exist_ok=True)
        path = os.path.join(results_dir, f"simulation_{simulation_id}_{timestamp}.json")
    
    # Convertir DataFrame a formato serializable
    if "results_df" in results and isinstance(results["results_df"], pd.DataFrame):
        results["results_df_dict"] = results["results_df"].to_dict(orient="records")
        del results["results_df"]
    
    # Guardar resultados
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    return path

def load_simulation_results(path):
    """
    Carga resultados de una simulación desde un archivo.
    
    Args:
        path: Ruta del archivo de resultados
    
    Returns:
        Diccionario con resultados
    """
    with open(path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Convertir datos a DataFrame si existe
    if "results_df_dict" in results:
        results["results_df"] = pd.DataFrame(results["results_df_dict"])
        del results["results_df_dict"]
    
    return results

def export_network_graph(organization, format="graphml", path=None):
    """
    Exporta el grafo de la organización a un archivo.
    
    Args:
        organization: Objeto Organization con el grafo
        format: Formato de exportación ("graphml", "gexf", "json")
        path: Ruta donde guardar el archivo (opcional)
    
    Returns:
        Ruta del archivo guardado
    """
    if not hasattr(organization, 'network') or not isinstance(organization.network, nx.Graph):
        raise ValueError("La organización no tiene un grafo de red válido")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if path is None:
        # Usar directorio por defecto
        network_dir = os.path.join("data", "networks")
        os.makedirs(network_dir, exist_ok=True)
        path = os.path.join(network_dir, f"network_{timestamp}.{format}")
    
    # Exportar según formato
    if format == "graphml":
        nx.write_graphml(organization.network, path)
    elif format == "gexf":
        nx.write_gexf(organization.network, path)
    elif format == "json":
        with open(path, 'w') as f:
            json.dump(nx.node_link_data(organization.network), f, indent=2)
    else:
        raise ValueError(f"Formato no soportado: {format}")
    
    return path

def generate_random_organization_data(num_agents=30, hierarchy_levels=3):
    """
    Genera datos aleatorios para una organización.
    Útil para hacer pruebas y demostraciones.
    
    Args:
        num_agents: Número total de agentes
        hierarchy_levels: Número de niveles jerárquicos
    
    Returns:
        Diccionario con datos organizacionales
    """
    # Distribuir agentes por nivel
    agents_per_level = {}
    total = 0
    
    # El nivel 0 siempre tiene 1 agente (CEO)
    agents_per_level[0] = 1
    total += 1
    
    # Distribuir el resto en forma de pirámide
    remaining = num_agents - 1
    for level in range(1, hierarchy_levels):
        # Más agentes en niveles inferiores
        if level == hierarchy_levels - 1:
            # El último nivel toma todos los restantes
            agents_per_level[level] = remaining
        else:
            # Niveles intermedios
            agents_per_level[level] = min(remaining, int(remaining * (0.3 * level)))
        
        total += agents_per_level[level]
        remaining = num_agents - total
    
    # Crear organización
    org_data = {
        "hierarchy_levels": hierarchy_levels,
        "total_agents": total,
        "agents_per_level": agents_per_level,
        "agents": []
    }
    
    # Crear agentes
    agent_id = 0
    for level in range(hierarchy_levels):
        for i in range(agents_per_level[level]):
            # Determinar tipo de agente según nivel
            if level == 0:
                agent_type = "Manager"
                role = "CEO"
            elif level == hierarchy_levels - 1:
                # Último nivel: principalmente workers con algunos innovadores
                agent_type = "Worker" if random.random() < 0.8 else "Innovator"
                role = agent_type
            else:
                # Niveles intermedios: principalmente managers
                agent_type = "Manager"
                role = "Executive" if level == 1 else "Middle Manager"
            
            # Añadir agente
            agent = {
                "id": f"A{agent_id}",
                "type": agent_type,
                "role": role,
                "level": level,
                "knowledge": round(random.uniform(0.3, 0.9), 2),
                "productivity": round(random.uniform(0.4, 0.8), 2) if agent_type == "Worker" else None,
                "decision_quality": round(random.uniform(0.5, 0.9), 2) if agent_type == "Manager" else None,
                "innovation_ability": round(random.uniform(0.2, 0.7), 2) if agent_type == "Innovator" else None
            }
            
            org_data["agents"].append(agent)
            agent_id += 1
    
    return org_data

def analyze_network(organization):
    """
    Analiza el grafo de la red organizacional y calcula métricas.
    
    Args:
        organization: Objeto Organization con el grafo
    
    Returns:
        Diccionario con métricas del análisis
    """
    G = organization.network
    
    # Calcular métricas básicas de la red
    metrics = {
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "density": nx.density(G),
        "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes()
    }
    
    # Calcular centralidad
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Identificar nodos más importantes
    metrics["most_central_nodes"] = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    metrics["most_between_nodes"] = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calcular componentes conexas
    metrics["connected_components"] = list(nx.connected_components(G.to_undirected()))
    metrics["strongly_connected_components"] = list(nx.strongly_connected_components(G)) if nx.is_directed(G) else []
    
    # Calcular agrupaciones
    try:
        metrics["clustering_coefficient"] = nx.average_clustering(G)
    except:
        metrics["clustering_coefficient"] = None
    
    return metrics