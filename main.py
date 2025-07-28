import subprocess
import threading
import os

def run_flask():
    os.system("python backend/main.py")

# def run_streamlit():
#     os.system("streamlit run front/app.py --server.port 8501")

threading.Thread(target=run_flask).start()
# run_streamlit()
