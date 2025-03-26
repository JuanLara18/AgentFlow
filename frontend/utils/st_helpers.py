import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def show_success_message(message, delay=2):
    """Muestra un mensaje de éxito con desaparición automática."""
    message_placeholder = st.empty()
    message_placeholder.success(message)
    # Note: Streamlit no permite sleep o timers para limpiar el mensaje después
    # Esta función servirá como referencia para implementaciones futuras con JS

def toggle_visibility(key, value=None):
    """Cambia o establece la visibilidad de un componente."""
    if value is not None:
        st.session_state[key] = value
    else:
        st.session_state[key] = not st.session_state.get(key, False)

def create_tab_container():
    """Crea un contenedor con tabs para organizar contenido."""
    tab_placeholder = st.empty()
    return tab_placeholder

def save_configuration(config_dict, file_type="json"):
    """Guarda una configuración en un archivo."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if file_type == "json":
        json_data = json.dumps(config_dict, indent=2)
        return json_data, f"agentflow_config_{timestamp}.json", "application/json"
    elif file_type == "csv":
        df = pd.DataFrame(config_dict)
        return df.to_csv(index=False), f"agentflow_config_{timestamp}.csv", "text/csv"
    else:
        raise ValueError(f"Tipo de archivo no soportado: {file_type}")

def load_configuration(uploaded_file):
    """Carga una configuración desde un archivo subido."""
    if uploaded_file is None:
        return None
    
    # Determinar el tipo de archivo
    if uploaded_file.name.endswith('.json'):
        # Cargar JSON
        config_dict = json.loads(uploaded_file.getvalue().decode('utf-8'))
        return config_dict
    elif uploaded_file.name.endswith('.csv'):
        # Cargar CSV
        df = pd.read_csv(uploaded_file)
        return df.to_dict(orient="records")
    else:
        st.error("Formato de archivo no soportado. Por favor sube un archivo JSON o CSV.")
        return None

def display_validation_error(message):
    """Muestra un mensaje de error de validación."""
    st.error(message)
    return False

def validate_budget_allocation(training_budget, innovation_budget):
    """Valida la asignación de presupuesto."""
    if training_budget + innovation_budget > 100:
        return display_validation_error("La asignación total de presupuesto no puede exceder el 100%")
    return True

def setup_session_state_defaults():
    """Configura valores por defecto en session_state si no existen."""
    defaults = {
        'current_scenario': None,
        'agents_config': {},
        'org_policies': {},
        'simulation_results': None,
        'page': "Scenario Setup",
        'annotations': [],
        
        # Scenario parameters
        'sim_duration': 100,
        'market_volatility': 0.3,
        'initial_capital': 100000,
        'training_cost': 1.0,
        'decision_freq': 5
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def format_metric_name(metric_name):
    """Formatea el nombre de una métrica para mostrar."""
    return metric_name.replace('_', ' ').title()