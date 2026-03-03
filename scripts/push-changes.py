#!/usr/bin/env python3
import subprocess
import sys

def run_command(cmd):
    """Run a shell command and print output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd="/vercel/share/v0-project")
    if result.returncode != 0:
        print(f"Error executing command: {cmd}")
        sys.exit(1)
    return result

print("Adding all changes...")
run_command("git add .")

print("\nCommitting changes...")
run_command('git commit -m "feat: Build complete IELTS Speaking AI frontend\n\n- Setup Next.js 14 with TypeScript and Tailwind CSS\n- Implement JWT-based authentication system with AuthContext\n- Create authentication pages (register, login, landing)\n- Build speaking test pages (Part 1, 2, 3) with voice recording\n- Implement results page with score visualization\n- Add circular countdown timers and audio recording utilities\n- Integrate with FastAPI backend\n- Add error handling and loading states\n- Responsive design with Framer Motion animations"')

print("\nPushing to ielts-ai-app branch...")
run_command("git push origin HEAD:ielts-ai-app")

print("\n✓ Changes pushed successfully to ielts-ai-app branch!")
