import subprocess
import time

import requests


def start_server():
    model_path = r"D:\Download\chatgpt-streamlit-master\sample-gpt-local-master\models\mistral-7b-openorca.Q4_K_M.gguf"
    host = "127.0.0.1"
    port = 8000
    # Construct the command
    command = [
        "python",
        "-m",
        "llama_cpp.server",
        "--model",
        model_path,
        "--chat_format",
        "chatml",
        "--n_gpu_layers",
        "1",
        "--host",
        host,
        "--port",
        str(port)
    ]

    # Start the server as a separate process
    process = subprocess.run(command, shell=True)
    return process




