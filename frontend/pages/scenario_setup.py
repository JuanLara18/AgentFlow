# Scenario Setup page implementationimport streamlit as st
import streamlit as st
from components.charts import sample_scenario_chart

def show_scenario_setup():
    st.header("Scenario Setup")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selector de escenario
        scenario_options = {
            "classic_hierarchy": "Classic Hierarchy",
            "innovation_driven": "Innovation-driven Structure",
            "decentralized": "Decentralized Training"
        }
        
        selected_scenario = st.selectbox(
            "Scenario Selector",
            options=list(scenario_options.keys()),
            format_func=lambda x: scenario_options[x]
        )
        
        # Resumen del escenario
        scenario_descriptions = {
            "classic_hierarchy": """
            **Classic Hierarchy** represents a traditional organizational structure with clear vertical 
            communication lines. Features multi-level management, specialized workers, and defined 
            roles for each agent.
            """,
            "innovation_driven": """
            **Innovation-driven Structure** prioritizes breakthrough development with dedicated 
            innovation teams. Features flexible hierarchies, resource allocation focused on R&D, and 
            knowledge sharing mechanisms.
            """,
            "decentralized": """
            **Decentralized Training** emphasizes horizontal knowledge transfer and autonomous teams. 
            Features minimal management layers, self-organizing worker groups, and distributed 
            decision-making processes.
            """
        }
        
        st.markdown(scenario_descriptions[selected_scenario])
        
        # Parámetros del escenario
        st.subheader("Scenario Parameters")
        
        with st.expander("Economic Parameters", expanded=True):
            st.slider("Initial Capital", 50000, 500000, 100000, 10000, key="initial_capital")
            st.slider("Market Volatility", 0.0, 1.0, 0.3, 0.1, key="market_volatility")
            st.number_input("Training Cost Multiplier", 0.5, 5.0, 1.0, 0.1, key="training_cost")
        
        with st.expander("Time Parameters", expanded=True):
            st.number_input("Simulation Duration (periods)", 10, 500, 100, 10, key="sim_duration")
            st.number_input("Decision Frequency", 1, 10, 5, 1, key="decision_freq")
        
        # Botón para cargar parámetros por defecto
        if st.button("Load Default Parameters"):
            if selected_scenario == "classic_hierarchy":
                st.session_state.initial_capital = 100000
                st.session_state.market_volatility = 0.2
                st.session_state.training_cost = 1.0
                st.session_state.sim_duration = 120
                st.session_state.decision_freq = 3
            elif selected_scenario == "innovation_driven":
                st.session_state.initial_capital = 150000
                st.session_state.market_volatility = 0.4
                st.session_state.training_cost = 1.5
                st.session_state.sim_duration = 100
                st.session_state.decision_freq = 2
            elif selected_scenario == "decentralized":
                st.session_state.initial_capital = 80000
                st.session_state.market_volatility = 0.3
                st.session_state.training_cost = 0.8
                st.session_state.sim_duration = 150
                st.session_state.decision_freq = 5
            
            st.success("Default parameters loaded!")
        
        # Guardar escenario
        if st.button("Save Scenario", type="primary"):
            st.session_state.current_scenario = selected_scenario
            st.success(f"Scenario '{scenario_options[selected_scenario]}' saved!")
    
    with col2:
        # Previsualización del escenario
        st.subheader("Scenario Preview")
        sample_scenario_chart(selected_scenario)
        
        # Escenarios guardados
        st.subheader("Saved Scenarios")
        if st.session_state.current_scenario:
            st.info(f"Active: {scenario_options[st.session_state.current_scenario]}")
        else:
            st.warning("No active scenario")