import optuna
import logging
import numpy as np
from backend.simulations.simulator import Simulator

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PolicyOptimizer:
    """Optimizador de políticas organizacionales utilizando Optuna."""
    
    def __init__(self, scenario_type, agent_config, iterations=1, periods=50):
        self.scenario_type = scenario_type
        self.agent_config = agent_config
        self.iterations = iterations
        self.periods = periods
        self.best_params = None
        self.best_value = None
    
    def objective(self, trial, target="Balanced"):
        """Función objetivo para Optuna."""
        # Crear simulador
        simulator = Simulator()
        simulator.setup_scenario(self.scenario_type)
        simulator.setup_agents(self.agent_config)
        
        # Definir espacio de búsqueda para los parámetros
        policy_params = {
            "centralization": trial.suggest_float("centralization", 0.1, 0.9),
            "training_budget": trial.suggest_int("training_budget", 10, 50),
            "innovation_budget": trial.suggest_int("innovation_budget", 5, 40),
            "vertical_comm": trial.suggest_float("vertical_comm", 0.3, 0.9),
            "horizontal_comm": trial.suggest_float("horizontal_comm", 0.2, 0.9),
            "hierarchy_depth": trial.suggest_int("hierarchy_depth", 2, 5),
            "span_of_control": trial.suggest_int("span_of_control", 3, 8)
        }
        
        # Comprobar restricción de presupuesto total
        if policy_params["training_budget"] + policy_params["innovation_budget"] > 70:
            policy_params["innovation_budget"] = max(5, 70 - policy_params["training_budget"])
        
        # Seleccionar método de asignación de tareas
        policy_params["task_allocation"] = trial.suggest_categorical(
            "task_allocation", 
            ["Skill-based", "Availability-based", "Balanced"]
        )
        
        # Seleccionar método de aprendizaje
        policy_params["learning_method"] = trial.suggest_categorical(
            "learning_method",
            ["Formal Training", "Peer Learning", "On-the-job Training", "Mixed"]
        )
        
        # Actualizar políticas
        simulator.update_policies(policy_params)
        
        # Ejecutar simulación
        results = simulator.run(iterations=self.iterations, periods=self.periods)
        
        # Calcular métricas objetivo según el target
        metrics = results["results_df"].groupby("iteration").mean()
        
        if target == "Productivity":
            objective_value = metrics["productivity"].mean()
        elif target == "Cost Efficiency":
            objective_value = metrics["cost_efficiency"].mean()
        elif target == "Innovation Rate":
            objective_value = metrics["innovation_rate"].mean()
        else:  # Balanced
            # Combinar métricas con pesos
            objective_value = (
                0.4 * metrics["productivity"].mean() +
                0.3 * metrics["cost_efficiency"].mean() +
                0.2 * metrics["innovation_rate"].mean() +
                0.1 * metrics["agent_satisfaction"].mean()
            )
        
        return objective_value
    
    def optimize(self, n_trials=30, target="Balanced"):
        """Ejecuta la optimización."""
        logger.info(f"Iniciando optimización para target: {target}")
        
        # Crear estudio Optuna
        study = optuna.create_study(direction="maximize")
        
        # Ejecutar optimización
        study.optimize(
            lambda trial: self.objective(trial, target), 
            n_trials=n_trials
        )
        
        self.best_params = study.best_params
        self.best_value = study.best_value
        
        logger.info(f"Optimización completada. Mejor valor: {study.best_value}")
        logger.info(f"Mejores parámetros: {study.best_params}")
        
        # Devolver resultados
        return {
            "best_params": study.best_params,
            "best_value": study.best_value,
            "all_trials": [
                {
                    "params": trial.params,
                    "value": trial.value
                }
                for trial in study.trials
            ]
        }