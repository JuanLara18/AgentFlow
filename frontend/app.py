import streamlit as st
from pages.scenario_setup import show_scenario_setup
from pages.agent_configuration import show_agent_configuration
from pages.organizational_policies import show_organizational_policies
from pages.simulation_execution import show_simulation_execution
from pages.analytics_visualization import show_analytics_visualization
from pages.export_reporting import show_export_reporting
from utils.st_helpers import setup_session_state_defaults

# Configuración de la página
st.set_page_config(
    page_title="AgentFlow",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize all default session state variables
setup_session_state_defaults()

# Inicialización de estado si no existe
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'agents_config' not in st.session_state:
    st.session_state.agents_config = {}
if 'org_policies' not in st.session_state:
    st.session_state.org_policies = {}
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None

# Inicialización de variables de escenario
if 'sim_duration' not in st.session_state:
    st.session_state.sim_duration = 100
if 'market_volatility' not in st.session_state:
    st.session_state.market_volatility = 0.3
if 'initial_capital' not in st.session_state:
    st.session_state.initial_capital = 100000
if 'training_cost' not in st.session_state:
    st.session_state.training_cost = 1.0
if 'decision_freq' not in st.session_state:
    st.session_state.decision_freq = 5

# Título principal
st.sidebar.title("AgentFlow")
st.sidebar.caption("Multi-Agent Simulation Framework")

# Navegación principal
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Navigation",
    ["Scenario Setup", "Agent Configuration", "Organizational Policies", 
     "Simulation Execution", "Analytics & Visualization", "Export & Reporting"],
    label_visibility="collapsed"
)

# Mostrar la página correspondiente
if page == "Scenario Setup":
    show_scenario_setup()
elif page == "Agent Configuration":
    show_agent_configuration()
elif page == "Organizational Policies":
    show_organizational_policies()
elif page == "Simulation Execution":
    show_simulation_execution()
elif page == "Analytics & Visualization":
    show_analytics_visualization()
elif page == "Export & Reporting":
    show_export_reporting()

# Información de estado en el sidebar (para debugging)
st.sidebar.markdown("---")
st.sidebar.markdown("### Current State")
if st.session_state.current_scenario:
    st.sidebar.success(f"Scenario: {st.session_state.current_scenario}")
else:
    st.sidebar.warning("No scenario selected")