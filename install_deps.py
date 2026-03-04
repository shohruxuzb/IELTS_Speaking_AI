#!/usr/bin/env python3
"""Install backend dependencies and setup environment."""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("IELTS Speaking AI - Backend Setup")
    print("=" * 60)
    
    # Get the absolute path to requirements.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, 'requirements.txt')
    
    print(f"\n📦 Installing dependencies from: {requirements_path}")
    
    if not os.path.exists(requirements_path):
        print(f"❌ Error: requirements.txt not found at {requirements_path}")
        sys.exit(1)
    
    try:
        # Install packages
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', requirements_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Installation failed:\n{result.stderr}")
            sys.exit(1)
        
        print("✅ Dependencies installed successfully!")
        print("\n🚀 You can now run the backend with:")
        print("   python main.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
