from dotenv import load_dotenv
from loguru import logger

import multiprocessing
import subprocess
import psutil
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please provide the environment as an argument: dev or prod")
        sys.exit(1)

    env = sys.argv[1]

    if env == "dev":
        load_dotenv(".env.dev", override=True)  
    elif env == "prod":
        load_dotenv(".env", override=True)  
    else:
        print("Invalid environment. Use 'dev' or 'prod'.")
        sys.exit(1)

    cpu_cores = multiprocessing.cpu_count()
    available_memory_gb = psutil.virtual_memory().available / (1024 ** 3) 
    workers = min(cpu_cores, int(available_memory_gb / 0.1), 2)
    
    try:
        logger.info(f"Server started on port {os.getenv('PORT_NUMBER')} with {workers} workers.")
        logger.info(f"Available CPU cores: {cpu_cores}")
        logger.info(f"Available memory: {available_memory_gb:.2f} GB")
        logger.info(f"Using {max(1, workers)} workers.")
        
        subprocess.run([
            "gunicorn",
            "app.main:app",
            "--bind", f"0.0.0.0:{os.getenv('PORT_NUMBER')}",
            "--reload",
            "--workers", f"{str(max(1, workers))}",
            "--worker-class", "uvicorn.workers.UvicornWorker",
            "--timeout", "60",
            "--worker-connections", "100",
            "--access-logfile", "-",  # Log to stdout
            "--error-logfile", "-",   # Log errors to stdout
            "--log-level", "debug",   # Set log level to debug
            "--capture-output",       # Capture print statements
        ])
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
        sys.exit(0)