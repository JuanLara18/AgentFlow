import time
import random

class Agent:
    """Clase base para todos los tipos de agentes."""
    
    def __init__(self, agent_id, knowledge_level=0.5):
        self.agent_id = agent_id
        self.knowledge_level = knowledge_level
        self.satisfaction = 0.7  # Nivel inicial de satisfacción
        self.tasks_completed = 0
        self.performance_history = []
    
    def perform_task(self, task):
        """
        Realiza una tarea y devuelve el resultado de rendimiento.
        
        Args:
            task: Objeto Task con información de la tarea
        
        Returns:
            dict: Diccionario con los resultados de la tarea
        """
        # Verificar si la tarea es válida
        if not task:
            return {"success": False, "message": "Tarea inválida", "performance": 0}
        
        # Calcular desempeño basado en dificultad y nivel de conocimiento
        difficulty_factor = task.difficulty or 0.5
        performance = min(1.0, self.knowledge_level * (1.0 / difficulty_factor))
        
        # Añadir factor aleatorio pequeño para simular variabilidad
        performance_with_variation = max(0, min(1.0, performance * (0.9 + random.random() * 0.2)))
        
        # Registrar la tarea completada
        self.tasks_completed += 1
        self.performance_history.append(performance_with_variation)
        
        # Calcular tiempo de ejecución basado en la dificultad y el desempeño
        execution_time = task.duration / performance_with_variation
        
        # Calcular calidad del resultado
        quality = performance_with_variation * (0.8 + 0.2 * random.random())
        
        # Preparar resultado
        result = {
            "task_id": task.task_id,
            "agent_id": self.agent_id,
            "performance": performance_with_variation,
            "quality": quality,
            "execution_time": execution_time,
            "timestamp": time.time(),
            "success": True
        }
        
        return result
    
    def update_satisfaction(self, org_support=0.5):
        """Actualiza el nivel de satisfacción del agente."""
        avg_performance = sum(self.performance_history[-5:]) / max(1, len(self.performance_history[-5:]))
        self.satisfaction = 0.3 * self.satisfaction + 0.5 * avg_performance + 0.2 * org_support
        return self.satisfaction
    
    def learn(self, learning_rate=0.05):
        """Incrementa el nivel de conocimiento del agente."""
        self.knowledge_level = min(1.0, self.knowledge_level + learning_rate)


class Manager(Agent):
    """Agente tipo Manager con capacidades de toma de decisiones."""
    
    def __init__(self, agent_id, knowledge_level=0.7, span_of_control=5, decision_quality=0.8):
        super().__init__(agent_id, knowledge_level)
        self.span_of_control = span_of_control
        self.decision_quality = decision_quality
        self.subordinates = []
    
    def make_decision(self, problem_complexity):
        """Toma una decisión basada en la complejidad del problema."""
        decision_score = self.knowledge_level * self.decision_quality * (1.0 / problem_complexity)
        return min(1.0, decision_score)
    
    def assign_subordinate(self, agent):
        """Asigna un agente como subordinado."""
        if len(self.subordinates) < self.span_of_control:
            self.subordinates.append(agent)
            return True
        return False


class Worker(Agent):
    """Agente tipo Worker con capacidades de producción."""
    
    def __init__(self, agent_id, knowledge_level=0.4, learning_rate=0.05, productivity=0.6):
        super().__init__(agent_id, knowledge_level)
        self.learning_rate = learning_rate
        self.productivity = productivity
        self.manager = None
    
    def produce(self, task_difficulty):
        """Produce resultados basados en la dificultad de la tarea."""
        output = self.productivity * self.knowledge_level * (1.0 / task_difficulty)
        return min(1.0, output)
    
    def learn_from_task(self, task_difficulty):
        """Aprende de la tarea realizada."""
        learning_gain = self.learning_rate * task_difficulty * 0.1
        self.knowledge_level = min(1.0, self.knowledge_level + learning_gain)


class Innovator(Agent):
    """Agente tipo Innovator con capacidades de innovación."""
    
    def __init__(self, agent_id, knowledge_level=0.8, discovery_probability=0.1, impact_factor=2.5):
        super().__init__(agent_id, knowledge_level)
        self.discovery_probability = discovery_probability
        self.impact_factor = impact_factor
        self.innovations = 0
    
    def attempt_innovation(self, resources_allocated):
        """Intenta generar una innovación basada en recursos y probabilidad."""
        innovation_chance = self.discovery_probability * resources_allocated * self.knowledge_level
        is_successful = innovation_chance > 0.5  # Simplificado para el ejemplo
        
        if is_successful:
            self.innovations += 1
            impact = self.impact_factor * self.knowledge_level * resources_allocated
            return True, impact
        
        return False, 0