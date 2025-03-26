import random
import networkx as nx
from collections import defaultdict

class Organization:
    """Modelo para representar la estructura organizacional."""
    
    def __init__(self, scenario_type, hierarchy_depth=3, span_of_control=5, centralization=0.5):
        self.scenario_type = scenario_type
        self.hierarchy_depth = hierarchy_depth
        self.span_of_control = span_of_control
        self.centralization = centralization
        self.capital = 0
        self.managers = []
        self.workers = []
        self.innovators = []
        self.all_agents = []
        self.network = nx.DiGraph()  # Grafo de la estructura organizacional
        self.communication_matrix = {}  # Matriz de comunicación entre agentes
    
    def add_agent(self, agent):
        """Añade un agente a la organización."""
        self.all_agents.append(agent)
        
        if agent.__class__.__name__ == "Manager":
            self.managers.append(agent)
        elif agent.__class__.__name__ == "Worker":
            self.workers.append(agent)
        elif agent.__class__.__name__ == "Innovator":
            self.innovators.append(agent)
        
        # Añadir nodo al grafo
        self.network.add_node(agent.agent_id, 
                             type=agent.__class__.__name__, 
                             knowledge=agent.knowledge_level)
    
    def build_hierarchy(self):
        """Construye la estructura jerárquica basada en los parámetros."""
        # Asegurarse de que hay al menos un manager
        if not self.managers:
            return
        
        # El primer manager es el CEO
        ceo = self.managers[0]
        level_agents = {0: [ceo]}
        
        # Construir niveles
        for level in range(1, self.hierarchy_depth):
            level_agents[level] = []
            
            # Asignar managers o workers a cada nivel
            agents_for_level = self.managers[1:] if level < self.hierarchy_depth - 1 else self.workers
            index = 0
            
            for parent in level_agents[level - 1]:
                # Determinar subordinados para este padre
                num_subordinates = min(self.span_of_control, len(agents_for_level) - index)
                
                for _ in range(num_subordinates):
                    if index < len(agents_for_level):
                        subordinate = agents_for_level[index]
                        
                        # Crear relación jerárquica
                        if hasattr(parent, 'assign_subordinate'):
                            parent.assign_subordinate(subordinate)
                        
                        if hasattr(subordinate, 'manager'):
                            subordinate.manager = parent
                        
                        # Añadir al grafo
                        self.network.add_edge(parent.agent_id, subordinate.agent_id, type="hierarchical")
                        
                        # Añadir a este nivel
                        level_agents[level].append(subordinate)
                        index += 1
        
        # Conectar innovadores según la centralización
        for innovator in self.innovators:
            # Con alta centralización, se conectan a niveles altos
            if random.random() < self.centralization:
                connect_to = level_agents[0][0]  # CEO
            else:
                # Seleccionar un nivel al azar (preferentemente bajo con baja centralización)
                level = random.choices(range(self.hierarchy_depth), 
                                      weights=[self.centralization**i for i in range(self.hierarchy_depth)])[0]
                if level_agents[level]:
                    connect_to = random.choice(level_agents[level])
                else:
                    connect_to = level_agents[0][0]  # Default CEO
            
            # Añadir conexión
            self.network.add_edge(connect_to.agent_id, innovator.agent_id, type="innovation")
            self.network.add_edge(innovator.agent_id, connect_to.agent_id, type="innovation")
    
    def build_communication_network(self, vertical_comm=0.7, horizontal_comm=0.4):
        """Construye la red de comunicación entre agentes."""
        # Inicializar matriz de comunicación
        for a1 in self.all_agents:
            for a2 in self.all_agents:
                if a1.agent_id != a2.agent_id:
                    self.communication_matrix[(a1.agent_id, a2.agent_id)] = 0.0
        
        # Añadir comunicación vertical (jerárquica)
        for edge in self.network.edges(data=True):
            if edge[2]['type'] == 'hierarchical':
                self.communication_matrix[(edge[0], edge[1])] = vertical_comm
                self.communication_matrix[(edge[1], edge[0])] = vertical_comm * 0.8  # Algo menor hacia arriba
        
        # Añadir comunicación horizontal (entre pares)
        node_levels = defaultdict(list)
        
        # Agrupar nodos por tipo para comunicación horizontal
        for agent in self.all_agents:
            node_levels[agent.__class__.__name__].append(agent.agent_id)
        
        # Conectar horizontalmente con cierta probabilidad
        for agent_type, nodes in node_levels.items():
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    if random.random() < horizontal_comm:
                        self.communication_matrix[(nodes[i], nodes[j])] = horizontal_comm
                        self.communication_matrix[(nodes[j], nodes[i])] = horizontal_comm
                        
                        # Añadir al grafo
                        self.network.add_edge(nodes[i], nodes[j], type="horizontal")
                        self.network.add_edge(nodes[j], nodes[i], type="horizontal")
    
    def allocate_budget(self, training_budget=0.3, innovation_budget=0.2):
        """Asigna presupuesto para formación e innovación."""
        total = self.capital
        training_allocation = total * training_budget
        innovation_allocation = total * innovation_budget
        operations_allocation = total - training_allocation - innovation_allocation
        
        return {
            "training": training_allocation,
            "innovation": innovation_allocation,
            "operations": operations_allocation
        }