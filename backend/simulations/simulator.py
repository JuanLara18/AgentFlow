import uuid
import random
import pandas as pd
from backend.core.engine import SimulationEngine
from backend.models.agents import Manager, Worker, Innovator
from backend.models.organization import Organization
from backend.models.policies import OrganizationalPolicies

class Simulator:
    """Orquestador principal de simulaciones."""
    
    def __init__(self):
        self.simulation_id = str(uuid.uuid4())
        self.engine = None
        self.organization = None
        self.policies = None
    
    def setup_scenario(self, scenario_type, params=None):
        """Configura el escenario de simulación según el tipo."""
        if params is None:
            params = {}
        
        # Valores por defecto
        default_params = {
            "initial_capital": 100000,
            "market_volatility": 0.3,
            "training_cost": 1.0,
            "sim_duration": 100,
            "decision_freq": 5
        }
        
        # Mezclar parámetros por defecto y proporcionados
        for key, value in default_params.items():
            if key not in params:
                params[key] = value
        
        # Configuración específica del escenario
        if scenario_type == "classic_hierarchy":
            hierarchy_depth = 3
            span_of_control = 5
            centralization = 0.7
            
            # Políticas para jerarquía clásica
            self.policies = OrganizationalPolicies()
            self.policies.centralization = 0.7
            self.policies.training_budget = 20
            self.policies.innovation_budget = 10
            self.policies.vertical_comm = 0.8
            self.policies.horizontal_comm = 0.3
            self.policies.task_allocation = "Skill-based"
            self.policies.learning_method = "Formal Training"
            
        elif scenario_type == "innovation_driven":
            hierarchy_depth = 3
            span_of_control = 4
            centralization = 0.5
            
            # Políticas para innovación
            self.policies = OrganizationalPolicies()
            self.policies.centralization = 0.5
            self.policies.training_budget = 25
            self.policies.innovation_budget = 30
            self.policies.vertical_comm = 0.6
            self.policies.horizontal_comm = 0.7
            self.policies.task_allocation = "Balanced"
            self.policies.learning_method = "Mixed"
            
        elif scenario_type == "decentralized":
            hierarchy_depth = 2
            span_of_control = 8
            centralization = 0.3
            
            # Políticas para estructura descentralizada
            self.policies = OrganizationalPolicies()
            self.policies.centralization = 0.3
            self.policies.training_budget = 35
            self.policies.innovation_budget = 15
            self.policies.vertical_comm = 0.5
            self.policies.horizontal_comm = 0.8
            self.policies.task_allocation = "Availability-based"
            self.policies.learning_method = "Peer Learning"
        
        else:
            raise ValueError(f"Tipo de escenario desconocido: {scenario_type}")
        
        # Crear organización
        self.organization = Organization(
            scenario_type, 
            hierarchy_depth, 
            span_of_control, 
            self.policies.centralization
        )
        
        # Actualizar parámetros en las políticas
        self.policies.hierarchy_depth = hierarchy_depth
        self.policies.span_of_control = span_of_control
        
        # Inicializar motor de simulación
        self.engine = SimulationEngine(
            self.organization,
            self.policies,
            params["initial_capital"],
            params["market_volatility"]
        )
    
    def setup_agents(self, agent_config):
        """Configura los agentes según la configuración proporcionada."""
        if not self.organization:
            raise ValueError("La organización no ha sido inicializada. Ejecute setup_scenario primero.")
        
        # Limpiar agentes existentes
        self.organization.managers = []
        self.organization.workers = []
        self.organization.innovators = []
        self.organization.all_agents = []
        
        # Configurar managers
        if "managers" in agent_config:
            config = agent_config["managers"]
            for i in range(config["quantity"]):
                manager = Manager(
                    f"M{i}",
                    knowledge_level=config["knowledge_level"],
                    span_of_control=config.get("span_of_control", 5),
                    decision_quality=config.get("decision_quality", 0.8)
                )
                self.organization.add_agent(manager)
        
        # Configurar workers
        if "workers" in agent_config:
            config = agent_config["workers"]
            for i in range(config["quantity"]):
                worker = Worker(
                    f"W{i}",
                    knowledge_level=config["knowledge_level"],
                    learning_rate=config.get("learning_rate", 0.05),
                    productivity=config.get("productivity", 0.6)
                )
                self.organization.add_agent(worker)
        
        # Configurar innovators
        if "innovators" in agent_config:
            config = agent_config["innovators"]
            for i in range(config["quantity"]):
                innovator = Innovator(
                    f"I{i}",
                    knowledge_level=config["knowledge_level"],
                    discovery_probability=config.get("discovery_probability", 0.1),
                    impact_factor=config.get("impact_factor", 2.5)
                )
                self.organization.add_agent(innovator)
        
        # Construir la estructura jerárquica y la red de comunicación
        self.organization.build_hierarchy()
        self.organization.build_communication_network(
            self.policies.vertical_comm,
            self.policies.horizontal_comm
        )
    
    def update_policies(self, policy_dict):
        """Actualiza las políticas con la configuración proporcionada."""
        if not self.policies:
            self.policies = OrganizationalPolicies()
        
        self.policies.update_from_dict(policy_dict)
        
        # Si la estructura jerárquica ha cambiado, reconstruirla
        if "hierarchy_depth" in policy_dict or "span_of_control" in policy_dict:
            self.organization.hierarchy_depth = self.policies.hierarchy_depth
            self.organization.span_of_control = self.policies.span_of_control
            self.organization.build_hierarchy()
        
        # Si la comunicación ha cambiado, actualizar la red
        if "vertical_comm" in policy_dict or "horizontal_comm" in policy_dict:
            self.organization.build_communication_network(
                self.policies.vertical_comm,
                self.policies.horizontal_comm
            )
    
    def run(self, iterations=1, periods=100):
        """Ejecuta la simulación con los parámetros configurados."""
        if not self.engine:
            raise ValueError("El motor de simulación no ha sido inicializado")
        
        results = []
        logs = []
        
        for i in range(iterations):
            # Reiniciar el motor para cada iteración
            if i > 0:
                self.engine = SimulationEngine(
                    self.organization,
                    self.policies,
                    self.engine.organization.capital,
                    self.engine.market_volatility
                )
            
            # Ejecutar simulación
            sim_result = self.engine.run_simulation(periods)
            
            # Agregar resultados
            for period_result in sim_result["results"]:
                period_result["iteration"] = i + 1
                results.append(period_result)
            
            # Agregar logs
            for log in sim_result["logs"]:
                logs.append(f"[Iteración {i+1}] {log}")
        
        # Crear DataFrame de resultados
        results_df = pd.DataFrame(results)
        
        return {
            "results_df": results_df,
            "logs": logs,
            "simulation_id": self.simulation_id
        }