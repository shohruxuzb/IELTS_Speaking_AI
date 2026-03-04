#!/usr/bin/env python3
"""
Setup script for IELTS Speaking AI backend
Installs dependencies and guides environment setup
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("=" * 60)
    print("IELTS Speaking AI - Backend Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Check for .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("\n⚠️  .env file not found!")
        print("\nYou need to create a .env file with the following variables:")
        print("  GROQ_API_KEY=your_groq_api_key_here")
        print("  JWT_SECRET_KEY=your_secret_key_here")
        print("  (Optional) DATABASE_URL, REDIS_URL, etc.")
        print("\nCreate .env file now? (y/n): ", end="")
        
        if input().lower() == 'y':
            with open(".env", "w") as f:
                f.write("# IELTS Speaking AI Environment Variables\n")
                f.write("GROQ_API_KEY=\n")
                f.write("JWT_SECRET_KEY=\n")
            print("✅ .env file created. Please edit it with your credentials.")
    else:
        print("✅ .env file found")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo start the backend, run:")
    print("  python main.py")
    print("\nThe backend will be available at http://localhost:8000")
    print("API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
