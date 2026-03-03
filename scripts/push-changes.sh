#!/bin/bash
set -e

echo "Adding all changes..."
git add .

echo "Committing changes..."
git commit -m "feat: Build complete IELTS Speaking AI frontend

- Setup Next.js 14 with TypeScript and Tailwind CSS
- Implement JWT-based authentication system with AuthContext
- Create authentication pages (register, login, landing)
- Build speaking test pages (Part 1, 2, 3) with voice recording
- Implement results page with score visualization
- Add circular countdown timers and audio recording utilities
- Integrate with FastAPI backend
- Add error handling and loading states
- Responsive design with Framer Motion animations"

echo "Pushing to ielts-ai-app branch..."
git push origin HEAD:ielts-ai-app

echo "Changes pushed successfully!"
