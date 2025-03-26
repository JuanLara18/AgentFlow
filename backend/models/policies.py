import random

class OrganizationalPolicies:
    """Modelo para las políticas organizacionales."""
    
    def __init__(self):
        # Parámetros base de políticas
        self.centralization = 0.5
        self.training_budget = 30  # Porcentaje
        self.innovation_budget = 20  # Porcentaje
        self.vertical_comm = 0.7
        self.horizontal_comm = 0.4
        self.hierarchy_depth = 3
        self.span_of_control = 5
        self.task_allocation = "Skill-based"
        self.learning_method = "Mixed"
    
    def update_from_dict(self, policy_dict):
        """Actualiza las políticas desde un diccionario de configuración."""
        for key, value in policy_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_learning_rate(self, agent):
        """Calcula la tasa de aprendizaje según el método de aprendizaje."""
        base_rate = getattr(agent, 'learning_rate', 0.05)
        
        if self.learning_method == "Formal Training":
            return base_rate * 1.5
        elif self.learning_method == "Peer Learning":
            return base_rate * (1.0 + 0.5 * self.horizontal_comm)
        elif self.learning_method == "On-the-job Training":
            return base_rate * (1.0 + 0.3 * agent.tasks_completed / max(1, 10))
        else:  # Mixed
            return base_rate * 1.2
    
    def allocate_task(self, tasks, agents):
        """Asigna tareas a agentes según la política de asignación."""
        assignments = {}
        
        if self.task_allocation == "Skill-based":
            # Ordenar tareas por dificultad (descendente)
            sorted_tasks = sorted(tasks, key=lambda t: t.difficulty, reverse=True)
            # Ordenar agentes por conocimiento (descendente)
            sorted_agents = sorted(agents, key=lambda a: a.knowledge_level, reverse=True)
            
            # Asignar tarea más difícil al agente más calificado
            for i, task in enumerate(sorted_tasks):
                if i < len(sorted_agents):
                    assignments[task.task_id] = sorted_agents[i].agent_id
        
        elif self.task_allocation == "Availability-based":
            # Asignar según la carga de trabajo actual
            agents_workload = {a.agent_id: len([t for t in assignments.values() if t == a.agent_id]) 
                              for a in agents}
            
            for task in tasks:
                if task.task_id not in assignments:
                    # Encontrar el agente con menor carga
                    agent_id = min(agents_workload.items(), key=lambda x: x[1])[0]
                    assignments[task.task_id] = agent_id
                    agents_workload[agent_id] += 1
        
        elif self.task_allocation == "Random":
            # Asignación aleatoria
            for task in tasks:
                if task.task_id not in assignments:
                    agent = random.choice(agents)
                    assignments[task.task_id] = agent.agent_id
        
        else:  # Balanced
            # Asignar balanceando habilidad y carga
            for task in tasks:
                if task.task_id not in assignments:
                    # Calcular puntaje combinado (80% habilidad, 20% disponibilidad)
                    scores = []
                    for agent in agents:
                        workload = len([t for t in assignments.values() if t == agent.agent_id])
                        skill_match = agent.knowledge_level / task.difficulty
                        balanced_score = 0.8 * skill_match + 0.2 * (1.0 / (workload + 1))
                        scores.append((agent.agent_id, balanced_score))
                    
                    # Asignar al agente con mejor puntaje
                    best_agent_id = max(scores, key=lambda x: x[1])[0]
                    assignments[task.task_id] = best_agent_id
        
        return assignments
    
    def calculate_communication_effectiveness(self, sender, receiver, organization):
        """Calcula la efectividad de comunicación entre dos agentes."""
        # Si la comunicación no está definida, devolver valor por defecto
        if (sender.agent_id, receiver.agent_id) not in organization.communication_matrix:
            return 0.2
        
        base_comm = organization.communication_matrix[(sender.agent_id, receiver.agent_id)]
        
        # Ajustar según centralización
        if self.centralization > 0.7:
            # Alta centralización favorece comunicación vertical
            if organization.network.has_edge(sender.agent_id, receiver.agent_id) and \
               organization.network[sender.agent_id][receiver.agent_id]['type'] == 'hierarchical':
                base_comm *= 1.2
        elif self.centralization < 0.3:
            # Baja centralización favorece comunicación horizontal
            if organization.network.has_edge(sender.agent_id, receiver.agent_id) and \
               organization.network[sender.agent_id][receiver.agent_id]['type'] == 'horizontal':
                base_comm *= 1.3
        
        return min(1.0, base_comm)