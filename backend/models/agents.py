class Agent:
    """Clase base para todos los tipos de agentes."""
    
    def __init__(self, agent_id, knowledge_level=0.5):
        self.agent_id = agent_id
        self.knowledge_level = knowledge_level
        self.satisfaction = 0.7  # Nivel inicial de satisfacción
        self.tasks_completed = 0
        self.performance_history = []
    
    def perform_task(self, task_difficulty):
        """Realiza una tarea y devuelve el resultado de rendimiento."""
        performance = min(1.0, self.knowledge_level * (1.0 / task_difficulty))
        self.tasks_completed += 1
        self.performance_history.append(performance)
        return performance
    
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