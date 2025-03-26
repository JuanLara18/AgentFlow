import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

def show_simulation_execution():
    st.header("Simulation Execution")
    
    # Verificar configuración previa
    if not st.session_state.current_scenario:
        st.warning("Please select a scenario first in the Scenario Setup page")
        return
    
    if not all(agent_type in st.session_state.agents_config for agent_type in ["managers", "workers", "innovators"]):
        st.warning("Please configure all agent types in the Agent Configuration page")
        return
    
    if not st.session_state.org_policies:
        st.warning("Please configure organizational policies in the Organizational Policies page")
        return
    
    # Mostrar resumen de configuración
    with st.expander("Configuration Summary", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Scenario")
            scenario_names = {
                "classic_hierarchy": "Classic Hierarchy",
                "innovation_driven": "Innovation-driven Structure",
                "decentralized": "Decentralized Training"
            }
            st.write(f"**Type:** {scenario_names[st.session_state.current_scenario]}")
            st.write(f"**Duration:** {st.session_state.sim_duration} periods")
            st.write(f"**Market Volatility:** {st.session_state.market_volatility}")
        
        with col2:
            st.subheader("Agents")
            managers = st.session_state.agents_config.get("managers", {})
            workers = st.session_state.agents_config.get("workers", {})
            innovators = st.session_state.agents_config.get("innovators", {})
            
            st.write(f"**Managers:** {managers.get('quantity', 0)}")
            st.write(f"**Workers:** {workers.get('quantity', 0)}")
            st.write(f"**Innovators:** {innovators.get('quantity', 0)}")
        
        with col3:
            st.subheader("Policies")
            policies = st.session_state.org_policies
            st.write(f"**Centralization:** {policies.get('centralization', 0)}")
            st.write(f"**Training Budget:** {policies.get('training_budget', 0)}%")
            st.write(f"**Learning Method:** {policies.get('learning_method', 'N/A')}")
    
    # Controles de simulación
    st.subheader("Simulation Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        iterations = st.number_input("Number of Iterations", min_value=1, max_value=100, value=3, step=1)
        random_seed = st.number_input("Random Seed", min_value=0, max_value=1000, value=42, step=1)
        
        use_optimization = st.checkbox("Enable Optimization", value=False)
        
        if use_optimization:
            optimization_target = st.selectbox(
                "Optimization Target",
                ["Productivity", "Cost Efficiency", "Innovation Rate", "Balanced"]
            )
            
            st.info("Optimization will tune policies to maximize the selected target")
    
    with col2:
        detailed_logging = st.checkbox("Enable Detailed Logging", value=True)
        real_time_updates = st.checkbox("Show Real-time Updates", value=True)
        
        export_format = st.selectbox(
            "Export Results Format",
            ["CSV", "Excel", "JSON", "None"]
        )
    
    # Botón para ejecutar la simulación
    if st.button("Execute Simulation", type="primary"):
        # Limpiar los resultados anteriores
        if 'simulation_results' in st.session_state:
            del st.session_state.simulation_results
        
        # Crear barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Crear panel de log
        log_container = st.container()
        with log_container:
            st.subheader("Simulation Log")
            log_output = st.empty()
        
        # Ejecutar simulación
        logs = []
        results = []
        
        start_time = datetime.now()
        
        # Simulación simulada
        for i in range(iterations):
            # Actualizar barra de progreso
            progress = (i + 1) / iterations
            progress_bar.progress(progress)
            status_text.text(f"Running iteration {i+1}/{iterations}...")
            
            # Generar registro de log
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Starting iteration {i+1}/{iterations}")
            
            # Simular pasos dentro de cada iteración
            steps = random.randint(10, 20)
            for step in range(steps):
                if real_time_updates:
                    # Simular tiempo de ejecución
                    time.sleep(0.1)
                    
                    # Agregar registro de actividad
                    activity = random.choice([
                        "Agent training completed",
                        "Task allocation optimized",
                        "Innovation discovery occurred",
                        "Management decision made",
                        "Resource reallocation executed"
                    ])
                    
                    logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {activity}")
                    
                    # Actualizar el panel de log
                    log_output.text("\n".join(logs[-10:]))  # Mostrar solo las últimas 10 entradas
            
            # Generar resultados simulados para esta iteración
            iteration_result = {
                "iteration": i + 1,
                "productivity": random.uniform(0.5, 1.0),
                "cost_efficiency": random.uniform(0.6, 0.9),
                "innovation_rate": random.uniform(0.1, 0.3),
                "agent_satisfaction": random.uniform(0.4, 0.8),
                "duration_seconds": random.randint(10, 30)
            }
            
            results.append(iteration_result)
            
            # Agregar registro de finalización
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Completed iteration {i+1} with productivity: {iteration_result['productivity']:.2f}")
            log_output.text("\n".join(logs[-10:]))
        
        # Finalizar la simulación
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Crear DataFrame de resultados
        results_df = pd.DataFrame(results)
        
        # Guardar resultados en session_state
        st.session_state.simulation_results = {
            "results_df": results_df,
            "logs": logs,
            "duration": duration,
            "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Mostrar resumen de resultados
        status_text.text(f"Simulation completed in {duration:.2f} seconds!")
        
        # Mostrar estadísticas de resumen
        st.subheader("Simulation Results Summary")
        st.dataframe(results_df)
        
        # Mensaje de finalización
        st.success("Simulation execution completed! You can now proceed to Analytics & Visualization to explore the results.")