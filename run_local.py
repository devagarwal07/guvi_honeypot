"""
Quick start script for local development.
"""

import subprocess
import sys
import os

def main():
    # Change to honeypot directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🍯 Starting Honeypot API locally...")
    print("=" * 50)
    print("API will be available at: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health: http://localhost:8000/health")
    print("=" * 50)
    print("\nPress Ctrl+C to stop\n")
    
    # Run uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    main()
