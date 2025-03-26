import os
import sys
import subprocess
import threading
import time

def run_api():
    print("Iniciando API Backend...")
    subprocess.run(["python", "run_api.py"])

def run_frontend():
    print("Iniciando Frontend Streamlit...")
    streamlit_script = os.path.join("frontend", "app.py")
    subprocess.run(["streamlit", "run", streamlit_script])

if __name__ == "__main__":
    # Iniciar el backend en un hilo separado
    api_thread = threading.Thread(target=run_api)
    api_thread.daemon = True
    api_thread.start()
    
    # Esperar un momento para que el backend inicie
    time.sleep(2)
    
    # Iniciar el frontend
    run_frontend()
