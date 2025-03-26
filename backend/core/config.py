import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del sistema
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configuración por defecto para simulaciones
DEFAULT_CONFIG = {
    "classic_hierarchy": {
        "initial_capital": 100000,
        "market_volatility": 0.2,
        "training_cost": 1.0,
        "sim_duration": 120,
        "decision_freq": 3
    },
    "innovation_driven": {
        "initial_capital": 150000,
        "market_volatility": 0.4,
        "training_cost": 1.5,
        "sim_duration": 100,
        "decision_freq": 2
    },
    "decentralized": {
        "initial_capital": 80000,
        "market_volatility": 0.3,
        "training_cost": 0.8,
        "sim_duration": 150,
        "decision_freq": 5
    }
}

# Rutas del sistema
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RESULTS_DIR = os.path.join(DATA_DIR, "results")

# Crear directorios si no existen
os.makedirs(RESULTS_DIR, exist_ok=True)