from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import json
from datetime import datetime

from backend.simulations.simulator import Simulator
from backend.simulations.optimization import PolicyOptimizer

# Modelos de datos para la API
class ScenarioParams(BaseModel):
    scenario_type: str
    initial_capital: int = 100000
    market_volatility: float = 0.3
    training_cost: float = 1.0
    sim_duration: int = 100
    decision_freq: int = 5

class AgentConfig(BaseModel):
    quantity: int
    knowledge_level: float
    additional_params: Dict[str, Any] = {}

class AgentsConfig(BaseModel):
    managers: Optional[AgentConfig] = None
    workers: Optional[AgentConfig] = None
    innovators: Optional[AgentConfig] = None

class OrganizationalPoliciesInput(BaseModel):
    centralization: float = 0.5
    training_budget: int = 30
    innovation_budget: int = 20
    vertical_comm: float = 0.7
    horizontal_comm: float = 0.4
    hierarchy_depth: int = 3
    span_of_control: int = 5
    task_allocation: str = "Skill-based"
    learning_method: str = "Mixed"

class SimulationParams(BaseModel):
    iterations: int = 1
    periods: int = 100
    random_seed: Optional[int] = None
    detailed_logging: bool = True

class OptimizationParams(BaseModel):
    target: str = "Balanced"
    n_trials: int = 30
    iterations: int = 1
    periods: int = 50

# Crear el router
router = APIRouter(prefix="/api", tags=["simulation"])

# Almacenamiento en memoria para simulaciones (en producción usaríamos una BD)
simulations_store = {}

# Endpoints
@router.post("/setup-scenario")
async def setup_scenario(params: ScenarioParams):
    """Configura un nuevo escenario de simulación."""
    simulator = Simulator()
    
    try:
        simulator.setup_scenario(
            params.scenario_type,
            {
                "initial_capital": params.initial_capital,
                "market_volatility": params.market_volatility,
                "training_cost": params.training_cost,
                "sim_duration": params.sim_duration,
                "decision_freq": params.decision_freq
            }
        )
        
        # Guardar el simulador en el almacenamiento
        simulation_id = simulator.simulation_id
        simulations_store[simulation_id] = simulator
        
        return {
            "simulation_id": simulation_id,
            "scenario_type": params.scenario_type,
            "message": "Escenario configurado correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/configure-agents/{simulation_id}")
async def configure_agents(simulation_id: str, config: AgentsConfig):
    """Configura los agentes para una simulación existente."""
    if simulation_id not in simulations_store:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    simulator = simulations_store[simulation_id]
    
    try:
        # Convertir a formato esperado por el simulador
        agent_config = {}
        
        if config.managers:
            agent_config["managers"] = {
                "quantity": config.managers.quantity,
                "knowledge_level": config.managers.knowledge_level,
                **config.managers.additional_params
            }
        
        if config.workers:
            agent_config["workers"] = {
                "quantity": config.workers.quantity,
                "knowledge_level": config.workers.knowledge_level,
                **config.workers.additional_params
            }
        
        if config.innovators:
            agent_config["innovators"] = {
                "quantity": config.innovators.quantity,
                "knowledge_level": config.innovators.knowledge_level,
                **config.innovators.additional_params
            }
        
        simulator.setup_agents(agent_config)
        
        return {
            "simulation_id": simulation_id,
            "message": "Agentes configurados correctamente",
            "agent_counts": {
                "managers": len(simulator.organization.managers),
                "workers": len(simulator.organization.workers),
                "innovators": len(simulator.organization.innovators)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/set-policies/{simulation_id}")
async def set_policies(simulation_id: str, policies: OrganizationalPoliciesInput):
    """Configura las políticas organizacionales para una simulación."""
    if simulation_id not in simulations_store:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    simulator = simulations_store[simulation_id]
    
    try:
        # Convertir a diccionario
        policy_dict = policies.dict()
        
        # Actualizar políticas
        simulator.update_policies(policy_dict)
        
        return {
            "simulation_id": simulation_id,
            "message": "Políticas configuradas correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/run-simulation/{simulation_id}")
async def run_simulation(simulation_id: str, params: SimulationParams):
    """Ejecuta una simulación configurada."""
    if simulation_id not in simulations_store:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    simulator = simulations_store[simulation_id]
    
    try:
        # Configurar semilla aleatoria si se proporciona
        if params.random_seed is not None:
            import random
            random.seed(params.random_seed)
        
        # Ejecutar simulación
        results = simulator.run(
            iterations=params.iterations,
            periods=params.periods
        )
        
        # Guardar solo los datos esenciales si no se requiere logging detallado
        if not params.detailed_logging:
            results["logs"] = results["logs"][-10:]  # Solo últimos 10 logs
        
        # Añadir timestamp
        timestamp = datetime.now().isoformat()
        results["timestamp"] = timestamp
        
        # Guardar resultados
        result_path = f"data/results/simulation_{simulation_id}_{timestamp}.json"
        
        try:
            with open(result_path, "w") as f:
                json.dump({
                    "simulation_id": simulation_id,
                    "results_summary": results["results_df"].describe().to_dict(),
                    "timestamp": timestamp,
                    "params": params.dict()
                }, f)
        except Exception as e:
            print(f"Error al guardar resultados: {e}")
        
        return {
            "simulation_id": simulation_id,
            "results": results,
            "message": "Simulación ejecutada correctamente",
            "result_path": result_path
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize-policies/{simulation_id}")
async def optimize_policies(simulation_id: str, params: OptimizationParams):
    """Optimiza las políticas para una simulación específica."""
    if simulation_id not in simulations_store:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    simulator = simulations_store[simulation_id]
    
    try:
        # Extraer configuración actual
        agent_config = {
            "managers": {
                "quantity": len(simulator.organization.managers),
                "knowledge_level": sum(m.knowledge_level for m in simulator.organization.managers) / 
                                 max(1, len(simulator.organization.managers))
            },
            "workers": {
                "quantity": len(simulator.organization.workers),
                "knowledge_level": sum(w.knowledge_level for w in simulator.organization.workers) / 
                                max(1, len(simulator.organization.workers))
            },
            "innovators": {
                "quantity": len(simulator.organization.innovators),
                "knowledge_level": sum(i.knowledge_level for i in simulator.organization.innovators) / 
                                max(1, len(simulator.organization.innovators))
            }
        }
        
        # Crear optimizador
        optimizer = PolicyOptimizer(
            simulator.organization.scenario_type,
            agent_config,
            iterations=params.iterations,
            periods=params.periods
        )
        
        # Ejecutar optimización
        results = optimizer.optimize(
            n_trials=params.n_trials,
            target=params.target
        )
        
        # Actualizar políticas con los mejores parámetros
        simulator.update_policies(results["best_params"])
        
        return {
            "simulation_id": simulation_id,
            "optimization_results": results,
            "message": "Optimización completada y políticas actualizadas"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/simulations")
async def list_simulations():
    """Lista todas las simulaciones disponibles."""
    return {
        "simulation_count": len(simulations_store),
        "simulations": [
            {
                "id": sim_id,
                "scenario_type": sim.organization.scenario_type if sim.organization else None,
                "agent_counts": {
                    "managers": len(sim.organization.managers) if sim.organization else 0,
                    "workers": len(sim.organization.workers) if sim.organization else 0,
                    "innovators": len(sim.organization.innovators) if sim.organization else 0
                } if sim.organization else None
            }
            for sim_id, sim in simulations_store.items()
        ]
    }

@router.delete("/simulations/{simulation_id}")
async def delete_simulation(simulation_id: str):
    """Elimina una simulación."""
    if simulation_id not in simulations_store:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    
    # Eliminar simulación
    del simulations_store[simulation_id]
    
    return {
        "message": f"Simulación {simulation_id} eliminada correctamente"
    }