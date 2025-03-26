import streamlit as st
import pandas as pd
import numpy as np

def agent_config_panel(agent_type, default_quantity=5, default_knowledge=0.5, additional_params=None):
    """
    Componente de configuración de agentes reutilizable.
    
    Args:
        agent_type: Tipo de agente ("managers", "workers", "innovators")
        default_quantity: Cantidad predeterminada de agentes
        default_knowledge: Nivel de conocimiento predeterminado
        additional_params: Diccionario con parámetros adicionales específicos
            Formato: {nombre_param: (min, max, default)}
    
    Returns:
        Diccionario con la configuración del agente
    """
    # Inicializar configuración o cargar existente
    if agent_type in st.session_state.agents_config:
        config = st.session_state.agents_config[agent_type]
    else:
        config = {
            "quantity": default_quantity,
            "knowledge_level": default_knowledge
        }
        
        # Añadir parámetros adicionales
        if additional_params:
            for param, (min_val, max_val, default) in additional_params.items():
                config[param] = default
    
    # Layout de dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Parámetros básicos
        config["quantity"] = st.number_input(
            "Quantity",
            min_value=1,
            max_value=100,
            value=config["quantity"],
            key=f"{agent_type}_quantity"
        )
        
        config["knowledge_level"] = st.slider(
            "Knowledge Level",
            min_value=0.0,
            max_value=1.0,
            value=float(config["knowledge_level"]),
            step=0.1,
            key=f"{agent_type}_knowledge"
        )
    
    with col2:
        # Parámetros adicionales específicos
        if additional_params:
            for param, (min_val, max_val, default) in additional_params.items():
                # Detectar el tipo de control apropiado según los valores
                if isinstance(min_val, int) and isinstance(max_val, int):
                    config[param] = st.number_input(
                        param.replace("_", " ").title(),
                        min_value=min_val,
                        max_value=max_val,
                        value=int(config.get(param, default)),
                        key=f"{agent_type}_{param}"
                    )
                else:
                    config[param] = st.slider(
                        param.replace("_", " ").title(),
                        min_value=float(min_val),
                        max_value=float(max_val),
                        value=float(config.get(param, default)),
                        step=0.01,
                        key=f"{agent_type}_{param}"
                    )
    
    # Vista previa de la configuración
    st.subheader("Agent Distribution Preview")
    
    # Generar datos simulados para la vista previa
    if agent_type == "managers":
        preview_data = pd.DataFrame({
            "Level": ["Senior", "Middle", "Junior"],
            "Count": [
                int(config["quantity"] * 0.2),
                int(config["quantity"] * 0.5),
                int(config["quantity"] * 0.3)
            ]
        })
    elif agent_type == "workers":
        preview_data = pd.DataFrame({
            "Level": ["Expert", "Senior", "Regular", "Junior", "Trainee"],
            "Count": [
                int(config["quantity"] * 0.1),
                int(config["quantity"] * 0.2),
                int(config["quantity"] * 0.4),
                int(config["quantity"] * 0.2),
                int(config["quantity"] * 0.1)
            ]
        })
    else:  # innovators
        preview_data = pd.DataFrame({
            "Level": ["Research Lead", "Senior Innovator", "Junior Innovator"],
            "Count": [
                int(config["quantity"] * 0.2),
                int(config["quantity"] * 0.5),
                int(config["quantity"] * 0.3)
            ]
        })
    
    # Mostrar datos de vista previa
    st.dataframe(preview_data, use_container_width=True)
    
    return config