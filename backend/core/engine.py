import random
import time
import logging
from collections import defaultdict

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Task:
    """Representa una tarea en la simulación."""
    
    def __init__(self, task_id, difficulty=0.5, importance=0.5, duration=1):
        self.task_id = task_id
        self.difficulty = difficulty
        self.importance = importance
        self.duration = duration
        self.status = "pending"  # pending, in_progress, completed
        self.assigned_to = None
        self.completion = 0.0
        self.results = None

class SimulationEngine:
    """Motor principal de simulación."""
    
    def __init__(self, organization, policies, initial_capital=100000, market_volatility=0.3):
        self.organization = organization
        self.policies = policies
        self.organization.capital = initial_capital
        self.market_volatility = market_volatility
        self.current_period = 0
        self.tasks = []
        self.task_history = []
        self.metrics = defaultdict(list)
        self.logs = []
    
    def log(self, message, level="INFO"):
        """Añade un mensaje al registro de la simulación."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        
        if level == "INFO":
            logger.info(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "ERROR":
            logger.error(message)
    
    def generate_tasks(self, num_tasks=None):
        """Genera tareas para el período actual."""
        if num_tasks is None:
            # Generar un número de tareas proporcional al tamaño de la organización
            num_tasks = max(5, len(self.organization.all_agents) // 2)
        
        for i in range(num_tasks):
            task_id = f"T{self.current_period}_{i}"
            difficulty = random.uniform(0.3, 0.9)
            importance = random.uniform(0.2, 1.0)
            duration = random.randint(1, 3)
            
            task = Task(task_id, difficulty, importance, duration)
            self.tasks.append(task)
            
            self.log(f"Generada tarea {task_id} con dificultad {difficulty:.2f}")
    
    def allocate_tasks(self):
        """Asigna las tareas pendientes a los agentes."""
        pending_tasks = [t for t in self.tasks if t.status == "pending"]
        available_agents = [a for a in self.organization.all_agents if a.__class__.__name__ == "Worker"]
        
        if not pending_tasks or not available_agents:
            return
        
        # Usar política de asignación de tareas
        assignments = self.policies.allocate_task(pending_tasks, available_agents)
        
        # Actualizar las asignaciones
        for task_id, agent_id in assignments.items():
            task = next((t for t in self.tasks if t.task_id == task_id), None)
            if task:
                task.assigned_to = agent_id
                task.status = "in_progress"
                self.log(f"Tarea {task_id} asignada al agente {agent_id}")
    
    def process_tasks(self):
        """Procesa las tareas en progreso."""
        in_progress = [t for t in self.tasks if t.status == "in_progress"]
        
        for task in in_progress:
            agent = next((a for a in self.organization.all_agents if a.agent_id == task.assigned_to), None)
            
            if not agent:
                continue
            
            # Calcular progreso de la tarea
            if agent.__class__.__name__ == "Worker":
                progress = agent.produce(task.difficulty) / task.duration
                task.completion += progress
                
                # Si se completa la tarea
                if task.completion >= 1.0:
                    task.status = "completed"
                    task.completion = 1.0
                    task.results = {
                        "quality": agent.knowledge_level * random.uniform(0.8, 1.0),
                        "time_efficiency": progress * random.uniform(0.9, 1.1)
                    }
                    self.task_history.append(task)
                    self.log(f"Tarea {task.task_id} completada por agente {agent.agent_id}")
                    
                    # Agente aprende de la tarea
                    learning_rate = self.policies.get_learning_rate(agent)
                    agent.learn_from_task(task.difficulty)
    
    def process_innovations(self):
        """Procesa intentos de innovación."""
        # Asignar recursos a innovadores
        budget = self.organization.allocate_budget(
            self.policies.training_budget / 100, 
            self.policies.innovation_budget / 100
        )
        
        innovation_resources = budget["innovation"]
        num_innovators = len(self.organization.innovators)
        
        if num_innovators == 0 or innovation_resources <= 0:
            return
        
        # Asignar recursos por innovador
        resources_per_innovator = innovation_resources / num_innovators
        
        total_innovations = 0
        total_impact = 0
        
        for innovator in self.organization.innovators:
            success, impact = innovator.attempt_innovation(resources_per_innovator / 10000)  # Normalizar
            
            if success:
                total_innovations += 1
                total_impact += impact
                self.log(f"Innovación lograda por {innovator.agent_id} con impacto {impact:.2f}")
        
        # Actualizar métricas
        if num_innovators > 0:
            self.metrics["innovation_rate"].append(total_innovations / num_innovators)
        else:
            self.metrics["innovation_rate"].append(0)
        
        self.metrics["innovation_impact"].append(total_impact)
    
    def update_agent_satisfaction(self):
        """Actualiza la satisfacción de los agentes."""
        # Calcular apoyo organizacional basado en políticas
        org_support = 0.5
        if self.policies.training_budget > 25:
            org_support += 0.2
        if self.policies.horizontal_comm > 0.5:
            org_support += 0.1
        
        # Actualizar satisfacción de cada agente
        satisfactions = []
        for agent in self.organization.all_agents:
            satisfaction = agent.update_satisfaction(org_support)
            satisfactions.append(satisfaction)
        
        # Actualizar métrica
        if satisfactions:
            self.metrics["agent_satisfaction"].append(sum(satisfactions) / len(satisfactions))
        else:
            self.metrics["agent_satisfaction"].append(0)
    
    def update_financial_metrics(self):
        """Actualiza métricas financieras y de productividad."""
        # Productividad basada en tareas completadas
        completed_tasks = [t for t in self.tasks if t.status == "completed"]
        productivity = len(completed_tasks) / max(1, len(self.tasks))
        
        # Calidad promedio
        quality = sum(t.results["quality"] for t in completed_tasks if t.results) / max(1, len(completed_tasks))
        
        # Cálculo simplificado de costos
        manager_cost = sum(10000 for _ in self.organization.managers)
        worker_cost = sum(5000 for _ in self.organization.workers)
        innovator_cost = sum(15000 for _ in self.organization.innovators)
        total_cost = manager_cost + worker_cost + innovator_cost
        
        # Ingresos simulados (basados en productividad, calidad e innovación)
        innovation_impact = self.metrics["innovation_impact"][-1] if self.metrics["innovation_impact"] else 0
        revenue_factor = productivity * quality * (1 + 0.2 * innovation_impact)
        revenue = 50000 * revenue_factor * (1 + random.uniform(-self.market_volatility, self.market_volatility))
        
        # Actualizar métricas
        self.metrics["productivity"].append(productivity)
        self.metrics["quality"].append(quality)
        self.metrics["revenue"].append(revenue)
        self.metrics["costs"].append(total_cost)
        self.metrics["profit"].append(revenue - total_cost)
        self.metrics["cost_efficiency"].append(revenue / max(1, total_cost))
    
    def clean_completed_tasks(self):
        """Elimina las tareas completadas de la lista activa."""
        self.tasks = [t for t in self.tasks if t.status != "completed"]
    
    def run_period(self):
        """Ejecuta un período completo de la simulación."""
        self.current_period += 1
        self.log(f"Iniciando período {self.current_period}")
        
        # Generar nuevas tareas
        self.generate_tasks()
        
        # Asignar tareas
        self.allocate_tasks()
        
        # Procesar tareas
        self.process_tasks()
        
        # Procesar innovaciones
        self.process_innovations()
        
        # Actualizar satisfacción
        self.update_agent_satisfaction()
        
        # Actualizar métricas financieras
        self.update_financial_metrics()
        
        # Limpiar tareas completadas
        self.clean_completed_tasks()
        
        self.log(f"Finalizado período {self.current_period}")
        
        # Devolver resumen del período
        return {
            "period": self.current_period,
            "productivity": self.metrics["productivity"][-1] if self.metrics["productivity"] else 0,
            "cost_efficiency": self.metrics["cost_efficiency"][-1] if self.metrics["cost_efficiency"] else 0,
            "innovation_rate": self.metrics["innovation_rate"][-1] if self.metrics["innovation_rate"] else 0,
            "agent_satisfaction": self.metrics["agent_satisfaction"][-1] if self.metrics["agent_satisfaction"] else 0,
            "tasks_completed": len([t for t in self.task_history if t.status == "completed" and 
                                   t.task_id.startswith(f"T{self.current_period}")]),
            "tasks_generated": len([t for t in self.tasks if t.task_id.startswith(f"T{self.current_period}")]) + 
                              len([t for t in self.task_history if t.task_id.startswith(f"T{self.current_period}")])
        }
    
    def run_simulation(self, num_periods):
        """Ejecuta la simulación completa por un número de períodos."""
        start_time = time.time()
        self.log(f"Iniciando simulación de {num_periods} períodos")
        
        results = []
        for _ in range(num_periods):
            period_result = self.run_period()
            results.append(period_result)
        
        duration = time.time() - start_time
        self.log(f"Simulación completada en {duration:.2f} segundos")
        
        return {
            "results": results,
            "metrics": dict(self.metrics),
            "logs": self.logs,
            "duration_seconds": duration
        }