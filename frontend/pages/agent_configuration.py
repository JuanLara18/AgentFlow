# Agent Configuration page implementationimport streamlit as st
import streamlit as st
from components.agent_editor import agent_config_panel

def show_agent_configuration():
    st.header("Agent Configuration")
    
    # Verificar si hay un escenario seleccionado
    if not st.session_state.current_scenario:
        st.warning("Please select a scenario first in the Scenario Setup page")
        if st.button("Go to Scenario Setup"):
            st.session_state.page = "Scenario Setup"
            st.experimental_rerun()
        return
    
    # Mostrar el escenario activo
    scenario_names = {
        "classic_hierarchy": "Classic Hierarchy",
        "innovation_driven": "Innovation-driven Structure",
        "decentralized": "Decentralized Training"
    }
    st.info(f"Configuring agents for: {scenario_names[st.session_state.current_scenario]}")
    
    # Tabs para diferentes tipos de agentes
    tabs = st.tabs(["Managers", "Workers", "Innovators"])
    
    # Configuración para Managers
    with tabs[0]:
        st.subheader("Manager Configuration")
        
        # Usar el componente de editor de agentes
        agent_config = agent_config_panel(
            agent_type="managers",
            default_quantity=3,
            default_knowledge=0.7,
            additional_params={
                "span_of_control": (3, 10, 5),
                "decision_quality": (0.1, 1.0, 0.8),
                "cost_per_manager": (5000, 15000, 10000)
            }
        )
        
        # Guardar configuración si se presiona el botón
        if st.button("Save Manager Configuration"):
            st.session_state.agents_config["managers"] = agent_config
            st.success("Manager configuration saved!")
    
    # Configuración para Workers
    with tabs[1]:
        st.subheader("Worker Configuration")
        
        # Usar el componente de editor de agentes
        agent_config = agent_config_panel(
            agent_type="workers",
            default_quantity=15,
            default_knowledge=0.4,
            additional_params={
                "learning_rate": (0.01, 0.2, 0.05),
                "productivity": (0.3, 1.0, 0.6),
                "cost_per_worker": (2000, 8000, 5000)
            }
        )
        
        # Guardar configuración si se presiona el botón
        if st.button("Save Worker Configuration"):
            st.session_state.agents_config["workers"] = agent_config
            st.success("Worker configuration saved!")
    
    # Configuración para Innovators
    with tabs[2]:
        st.subheader("Innovator Configuration")
        
        # Usar el componente de editor de agentes
        agent_config = agent_config_panel(
            agent_type="innovators",
            default_quantity=2,
            default_knowledge=0.8,
            additional_params={
                "discovery_probability": (0.01, 0.3, 0.1),
                "impact_factor": (1.0, 5.0, 2.5),
                "cost_per_innovator": (10000, 25000, 15000)
            }
        )
        
        # Guardar configuración si se presiona el botón
        if st.button("Save Innovator Configuration"):
            st.session_state.agents_config["innovators"] = agent_config
            st.success("Innovator configuration saved!")
    
    # Botón para guardar toda la configuración
    st.markdown("---")
    if st.button("Save All Agent Configurations", type="primary"):
        # Verificar que se han configurado todos los tipos de agentes
        if all(agent_type in st.session_state.agents_config for agent_type in ["managers", "workers", "innovators"]):
            st.balloons()
            st.success("All agent configurations saved successfully!")
        else:
            st.warning("Please configure all agent types before saving")