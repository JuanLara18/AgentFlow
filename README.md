# AgentFlow - Multi-Agent Simulation Framework

AgentFlow is a comprehensive multi-agent simulation framework specialized in modeling organizational economics and strategic management. This platform allows researchers, managers, and decision-makers to simulate complex organizational dynamics, experiment with different structures and policies, and analyze their impact on performance metrics.

![AgentFlow Banner](https://via.placeholder.com/1200x300/0272BA/FFFFFF?text=AgentFlow+Multi-Agent+Simulation)

## Table of Contents

- [AgentFlow - Multi-Agent Simulation Framework](#agentflow---multi-agent-simulation-framework)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Getting Started](#getting-started)
    - [Quick Start Guide](#quick-start-guide)
    - [Sample Workflow](#sample-workflow)
  - [Core Components](#core-components)
    - [Simulation Engine](#simulation-engine)
    - [Agent Models](#agent-models)
      - [Manager](#manager)
      - [Worker](#worker)
      - [Innovator](#innovator)
    - [Organizational Structures](#organizational-structures)
    - [Policies](#policies)
  - [Visualization \& Analytics](#visualization--analytics)
    - [Network Analysis](#network-analysis)
    - [Performance Charts](#performance-charts)
    - [Heat Maps](#heat-maps)
    - [Comparative Analysis](#comparative-analysis)
  - [Mathematical Models](#mathematical-models)
    - [Task Allocation](#task-allocation)
    - [Innovation Probability](#innovation-probability)
    - [Agent Learning](#agent-learning)
    - [Communication Effectiveness](#communication-effectiveness)
  - [Examples](#examples)
    - [Example 1: Comparing Organizational Structures](#example-1-comparing-organizational-structures)
    - [Example 2: Policy Optimization](#example-2-policy-optimization)
  - [API Reference](#api-reference)
    - [REST API Endpoints](#rest-api-endpoints)
    - [Python API](#python-api)
  - [Contributing](#contributing)
  - [License](#license)

## Overview

AgentFlow simulates the behavior of complex organizations composed of multiple interacting agents with different roles, capabilities, and objectives. By leveraging advanced agent-based modeling techniques, AgentFlow helps understand how organizational policies, communication patterns, and hierarchical structures affect overall performance, innovation rates, and cost efficiency.

The framework enables users to:

1. Design and configure different organizational scenarios
2. Simulate agent interactions under varying conditions
3. Analyze performance metrics and emergent behaviors
4. Visualize organizational structures and dynamics
5. Optimize policies for specific outcomes

## Features

- **Multiple Agent Types**: Managers, Workers, and Innovators with customizable attributes
- **Flexible Organizational Structures**: Hierarchy depth, span of control, and centralization level
- **Dynamic Policy Configuration**: Control budget allocation, communication patterns, and task allocation strategies
- **Interactive Visualizations**: Network graphs, heat maps, and performance charts
- **Policy Optimization**: Automated tuning of organizational parameters to maximize desired outcomes
- **Comprehensive Analytics**: Track productivity, innovation, cost efficiency, and agent satisfaction
- **Modular Architecture**: Easily extend with custom scenarios, agent types, and metrics

## Architecture

AgentFlow follows a modern, modular architecture:

```
AgentFlow/
├── backend/              # Simulation backend
│   ├── api/              # FastAPI endpoints
│   ├── core/             # Core engine and configuration
│   ├── models/           # Agent and organization models
│   ├── simulations/      # Simulation and optimization logic
│   └── utils/            # Utility functions
├── frontend/             # Streamlit web interface
│   ├── components/       # Reusable UI components
│   ├── pages/            # Application pages
│   └── utils/            # Frontend utilities
├── data/                 # Data storage
└── tests/                # Test suite
```

The platform uses a client-server design pattern:
- **Backend**: FastAPI-powered simulation engine and API endpoints
- **Frontend**: Streamlit-based interactive user interface
- **Communication**: RESTful API calls between frontend and backend

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/JuanLara18/agentflow.git
   cd agentflow
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit the .env file with your settings
   ```

5. Run the application:
   ```bash
   # Run both frontend and backend
   python run_all.py
   
   # Or run them separately
   python run_api.py      # Backend API
   python run_app.py      # Frontend
   ```

## Getting Started

### Quick Start Guide

1. **Scenario Setup**: Begin by selecting and configuring a simulation scenario
2. **Agent Configuration**: Define the number and attributes of managers, workers, and innovators
3. **Organizational Policies**: Set policies for centralization, communication, and task allocation
4. **Simulation Execution**: Run the simulation with your chosen parameters
5. **Analytics & Visualization**: Explore results and insights through interactive visualizations

### Sample Workflow

Here's a typical workflow for using AgentFlow:

1. Start with the "Classic Hierarchy" scenario
2. Configure 5 managers, 20 workers, and 3 innovators
3. Set a medium centralization level (0.5) and high vertical communication (0.7)
4. Run the simulation for 100 periods with 3 iterations
5. Analyze productivity trends and network patterns
6. Adjust organizational policies and re-run to compare outcomes

## Core Components

### Simulation Engine

The `SimulationEngine` class in `backend/core/engine.py` is the central component that orchestrates the simulation process. It manages:

- Task generation and allocation
- Agent interactions and productivity
- Innovation attempts and knowledge transfer
- Resource allocation and financial metrics
- Time progression through simulation periods

The engine uses a discrete-time simulation approach where each period represents a unit of organizational activity (e.g., a week or month).

### Agent Models

AgentFlow provides three base agent types:

#### Manager

Managers focus on decision-making and supervision. Their key attributes include:

- `knowledge_level`: Domain expertise (0-1)
- `decision_quality`: Quality of decisions made (0-1)
- `span_of_control`: Number of subordinates
- `satisfaction`: Current job satisfaction level

```python
# Creating a manager
manager = Manager(
    agent_id="M1",
    knowledge_level=0.7,
    span_of_control=5,
    decision_quality=0.8
)
```

#### Worker

Workers are responsible for task execution and production. Their attributes include:

- `knowledge_level`: Skill level (0-1)
- `learning_rate`: Speed of knowledge acquisition
- `productivity`: Base output rate
- `satisfaction`: Current job satisfaction level

#### Innovator

Innovators drive organizational advancement through new ideas. Their attributes include:

- `knowledge_level`: Domain expertise (0-1)
- `discovery_probability`: Chance of innovation success
- `impact_factor`: Potential impact of innovations
- `satisfaction`: Current job satisfaction level

### Organizational Structures

The `Organization` class in `backend/models/organization.py` defines the organizational structure and relationships between agents. Key components include:

- Hierarchical levels and reporting lines
- Communication networks and information flow
- Resource allocation mechanisms
- Task distribution systems

Three predefined organizational structures are available:

1. **Classic Hierarchy**: Traditional pyramid structure with clear authority lines
2. **Innovation-driven**: Flexible structure optimized for creative output
3. **Decentralized**: Flat organization with distributed decision-making

### Policies

The `OrganizationalPolicies` class in `backend/models/policies.py` defines the rules and parameters governing organizational behavior:

- `centralization`: Level of decision authority concentration (0-1)
- `training_budget`: Percentage of resources allocated to training
- `innovation_budget`: Percentage of resources allocated to innovation
- `vertical_comm`: Strength of communication between hierarchical levels
- `horizontal_comm`: Strength of communication between peers
- `task_allocation`: Method for assigning tasks ("Skill-based", "Availability-based", "Balanced")
- `learning_method`: Approach to knowledge acquisition ("Formal Training", "Peer Learning", "Mixed")

## Visualization & Analytics

AgentFlow provides powerful visualization tools to understand simulation results:

### Network Analysis

Visualize organizational structures as interactive network graphs where:
- Nodes represent agents
- Edges represent reporting lines and communication channels
- Colors indicate agent types and roles
- Edge thickness represents communication intensity

### Performance Charts

Track key performance indicators over time:
- Productivity evolution
- Innovation rates
- Cost efficiency
- Agent satisfaction

### Heat Maps

Analyze task allocation patterns across:
- Agent types
- Time periods
- Task categories

### Comparative Analysis

Compare the relationship between different metrics to identify:
- Correlations between variables
- Optimal policy configurations
- Performance tradeoffs

## Mathematical Models

AgentFlow implements several mathematical models to simulate organizational dynamics:

### Task Allocation

The task allocation function $A(t, a)$ assigns tasks $t$ to agents $a$ based on the selected policy:

For skill-based allocation:
$$A(t, a) = \arg\max_{a \in A} \frac{K_a}{D_t}$$

Where:
- $K_a$ is the knowledge level of agent $a$
- $D_t$ is the difficulty of task $t$

### Innovation Probability

The probability of successful innovation is modeled as:

$$P(\text{innovation}) = P_d \times R_a \times K_i$$

Where:
- $P_d$ is the base discovery probability
- $R_a$ is the resources allocated
- $K_i$ is the innovator's knowledge level

### Agent Learning

Knowledge acquisition follows:

$$K_{t+1} = \min(1.0, K_t + L_r \times D_t \times 0.1)$$

Where:
- $K_t$ is the knowledge at time $t$
- $L_r$ is the learning rate
- $D_t$ is the task difficulty

### Communication Effectiveness

Communication effectiveness between agents is calculated as:

$$E_{comm}(a_1, a_2) = B_{comm} \times F_{type} \times F_{cent}$$

Where:
- $B_{comm}$ is the base communication strength
- $F_{type}$ is the factor based on communication type (vertical/horizontal)
- $F_{cent}$ is the centralization adjustment factor

## Examples

### Example 1: Comparing Organizational Structures

```python
from backend.simulations.simulator import Simulator

# Create simulator instances for different structures
classic_sim = Simulator()
classic_sim.setup_scenario("classic_hierarchy")

innovation_sim = Simulator()
innovation_sim.setup_scenario("innovation_driven")

decentralized_sim = Simulator()
decentralized_sim.setup_scenario("decentralized")

# Configure identical agent distributions
agent_config = {
    "managers": {"quantity": 5, "knowledge_level": 0.7},
    "workers": {"quantity": 20, "knowledge_level": 0.5},
    "innovators": {"quantity": 3, "knowledge_level": 0.8}
}

# Setup agents for each simulator
classic_sim.setup_agents(agent_config)
innovation_sim.setup_agents(agent_config)
decentralized_sim.setup_agents(agent_config)

# Run simulations
classic_results = classic_sim.run(iterations=5, periods=100)
innovation_results = innovation_sim.run(iterations=5, periods=100)
decentralized_results = decentralized_sim.run(iterations=5, periods=100)

# Compare results
compare_productivity(classic_results, innovation_results, decentralized_results)
```

### Example 2: Policy Optimization

```python
from backend.simulations.optimization import PolicyOptimizer

# Create optimizer
optimizer = PolicyOptimizer(
    scenario_type="innovation_driven",
    agent_config=agent_config,
    iterations=3,
    periods=50
)

# Run optimization targeting innovation rate
results = optimizer.optimize(
    n_trials=30,
    target="Innovation Rate"
)

# Apply optimal policies
simulator = Simulator()
simulator.setup_scenario("innovation_driven")
simulator.setup_agents(agent_config)
simulator.update_policies(results["best_params"])

# Run with optimized policies
optimized_results = simulator.run(iterations=5, periods=100)
```

## API Reference

### REST API Endpoints

AgentFlow provides a RESTful API for programmatic access:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/setup-scenario` | POST | Configure a new simulation scenario |
| `/api/configure-agents/{simulation_id}` | POST | Set up agents for a simulation |
| `/api/set-policies/{simulation_id}` | POST | Configure organizational policies |
| `/api/run-simulation/{simulation_id}` | POST | Execute a simulation |
| `/api/optimize-policies/{simulation_id}` | POST | Optimize policies for a target |
| `/api/simulations` | GET | List all available simulations |
| `/api/simulations/{simulation_id}` | DELETE | Remove a simulation |

### Python API

The core simulation components can be imported and used directly:

```python
from backend.simulations.simulator import Simulator
from backend.models.agents import Manager, Worker, Innovator
from backend.models.organization import Organization
from backend.models.policies import OrganizationalPolicies

# Create custom simulation
simulator = Simulator()
simulator.setup_scenario("custom", {
    "initial_capital": 200000,
    "market_volatility": 0.4
})

# Add custom agents
organization = simulator.organization
organization.add_agent(Manager("M1", knowledge_level=0.9))
organization.add_agent(Worker("W1", productivity=0.8))

# Run simulation
results = simulator.run(periods=200)
```

## Contributing

We welcome contributions to AgentFlow! Here's how you can help:

1. **Report Issues**: Submit bugs and feature requests through the issue tracker
2. **Improve Documentation**: Enhance explanations, add examples, or fix errors
3. **Add Features**: Implement new agent types, policies, or visualization methods
4. **Optimize Code**: Improve performance or clean up existing code

Please follow our contribution guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

AgentFlow is released under the MIT License. See the LICENSE file for details.

---

For questions, support, or feedback, please contact [larajuand@outlook.com](mailto:larajuand@outlook.com) or open an issue on our GitHub repository.