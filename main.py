import subprocess
import threading
import time
from dotenv import load_dotenv

load_dotenv()
def run_backend():
    subprocess.run(["uvicorn","backend.main:app","--host","127.0.0.1","--port","8000"], check=True)

def run_frontend():
    subprocess.run(["streamlit","run","frontend.py"], check=True)

if __name__ == "__main__":
    threading.Thread(target=run_backend).start()
    time.sleep(2)
    run_frontend()
