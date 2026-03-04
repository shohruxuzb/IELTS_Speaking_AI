#!/usr/bin/env python3
import subprocess
import sys

print("=" * 60)
print("IELTS Speaking AI - Installing Dependencies")
print("=" * 60)

# List of packages from requirements.txt
packages = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "sqlalchemy",
    "python-multipart",
    "groq",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "python-dotenv",
]

print(f"\nInstalling {len(packages)} packages...")
print("-" * 60)

for package in packages:
    print(f"Installing {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", package],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✓ {package} installed successfully")
    else:
        print(f"✗ Failed to install {package}")
        print(result.stderr)

print("-" * 60)
print("\n✓ All dependencies installed successfully!")
print("\nYou can now run the backend with:")
print("  python main.py")
print("\nThe server will start on http://localhost:8000")
