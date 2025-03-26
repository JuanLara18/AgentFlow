import streamlit as st
from components.network_graph import display_organization_graph

def show_organizational_policies():
    st.header("Organizational Policies")
    
    # Verificar si hay un escenario y agentes configurados
    if not st.session_state.current_scenario:
        st.warning("Please select a scenario first in the Scenario Setup page")
        return
    
    if not all(agent_type in st.session_state.agents_config for agent_type in ["managers", "workers", "innovators"]):
        st.warning("Please configure all agent types in the Agent Configuration page")
        return
    
    # Layout con dos columnas
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Policy Configuration")
        
        # Centralización
        centralization = st.slider(
            "Centralization Level",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Determines how decisions are made (0: fully decentralized, 1: fully centralized)"
        )
        
        # Asignación de presupuesto
        st.subheader("Budget Allocation")
        col_a, col_b = st.columns(2)
        with col_a:
            training_budget = st.number_input(
                "Training Budget (%)",
                min_value=0,
                max_value=100,
                value=30,
                step=5,
                help="Percentage of budget allocated to training"
            )
        with col_b:
            innovation_budget = st.number_input(
                "Innovation Budget (%)",
                min_value=0,
                max_value=100,
                value=20,
                step=5,
                help="Percentage of budget allocated to innovation"
            )
        
        # Verificar que los presupuestos no excedan el 100%
        if training_budget + innovation_budget > 100:
            st.error("Total budget allocation cannot exceed 100%")
        
        # Intensidad de comunicación
        st.subheader("Communication Intensity")
        vertical_comm = st.slider(
            "Vertical Communication",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Intensity of communication between hierarchical levels"
        )
        
        horizontal_comm = st.slider(
            "Horizontal Communication",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help="Intensity of communication between agents in the same level"
        )
        
        # Estructura jerárquica
        st.subheader("Hierarchical Structure")
        hierarchy_depth = st.slider(
            "Hierarchy Depth",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="Number of hierarchical levels in the organization"
        )
        
        span_of_control = st.slider(
            "Span of Control",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
            help="Average number of subordinates per manager"
        )
        
        # Reglas de asignación de tareas
        st.subheader("Task Allocation Rules")
        task_allocation = st.selectbox(
            "Task Allocation Method",
            options=["Skill-based", "Availability-based", "Random", "Balanced"],
            index=0,
            help="Method used to assign tasks to agents"
        )
        
        # Políticas de aprendizaje
        st.subheader("Learning Policies")
        learning_method = st.selectbox(
            "Learning Method",
            options=["Formal Training", "Peer Learning", "On-the-job Training", "Mixed"],
            index=3,
            help="Method used for agent knowledge improvement"
        )
        
        # Guardar políticas
        if st.button("Save Organizational Policies", type="primary"):
            st.session_state.org_policies = {
                "centralization": centralization,
                "training_budget": training_budget,
                "innovation_budget": innovation_budget,
                "vertical_comm": vertical_comm,
                "horizontal_comm": horizontal_comm,
                "hierarchy_depth": hierarchy_depth,
                "span_of_control": span_of_control,
                "task_allocation": task_allocation,
                "learning_method": learning_method
            }
            st.success("Organizational policies saved successfully!")
    
    with col2:
        st.subheader("Organization Structure")
        # Mostrar la visualización de la estructura organizacional
        display_organization_graph(
            hierarchy_depth=hierarchy_depth,
            span_of_control=span_of_control,
            centralization=centralization,
            vertical_comm=vertical_comm,
            horizontal_comm=horizontal_comm
        )