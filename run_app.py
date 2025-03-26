import os
import sys
import subprocess

if __name__ == "__main__":
    # Ejecutar la aplicación Streamlit
    streamlit_script = os.path.join("frontend", "app.py")
    subprocess.run(["streamlit", "run", streamlit_script])
