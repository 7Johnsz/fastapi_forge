from dotenv import load_dotenv
from loguru import logger

import subprocess
import sys
import os

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            print("Please provide the environment as an argument: dev or prod")
            sys.exit(1)

        env = sys.argv[1]

        if env == "dev":
            load_dotenv(".env.dev", override=True) 
            os.environ["APP_ENV"] = ".env.dev"
            
            subprocess.run([
                "fastapi",
                "dev",
                "--port", f"{os.getenv('PORT_NUMBER')}",
                "app/main.py"
            ])
            
        elif env == "prod":
            load_dotenv(".env", override=True)  
            os.environ["APP_ENV"] = ".env"
            
            subprocess.run([
                "fastapi",
                "run",
                "--port", f"{os.getenv('PORT_NUMBER')}",
                "app/main.py"
            ])
        else:
            print("Invalid environment. Use 'dev' or 'prod'.")
            sys.exit(1)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
        sys.exit(0)