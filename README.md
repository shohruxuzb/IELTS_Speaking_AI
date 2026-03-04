# IELTS Speaking AI - Frontend

A modern, AI-powered IELTS Speaking practice platform built with Next.js, React, and Tailwind CSS.

## Features

- **User Authentication**: JWT-based authentication with secure token management
- **Speaking Practice**: Three-part test with voice recording (Part 1, Part 2, Part 3)
- **AI Evaluation**: Instant feedback on pronunciation, fluency, vocabulary, and grammar
- **Interactive Timers**: Precise countdown timers for Part 2 preparation and speaking phases
- **Detailed Results**: Comprehensive score breakdown with strengths and areas for improvement
- **Responsive Design**: Mobile-first, fully responsive user interface
- **Smooth Animations**: Framer Motion animations for enhanced UX

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **API**: RESTful API integration with Python FastAPI backend

## Getting Started

### Prerequisites

- Node.js 16.8 or later
- npm, yarn, or pnpm

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ielts-speaking-ai
```

2. Install dependencies:
```bash
npm install
# or
pnpm install
# or
yarn install
```

3. Set up environment variables:
```bash
# Create .env.local with the backend API URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**Environment Variables:**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: `http://localhost:8000` for local development)
  - For production, update to your deployed backend URL (e.g., `https://your-api.vercel.app`)
```

4. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

```
app/
  ├── page.tsx                 # Landing page
  ├── login/page.tsx           # Login page
  ├── register/page.tsx        # Registration page
  ├── speaking/
  │   ├── layout.tsx           # Speaking test layout
  │   ├── part1/page.tsx       # Introduction & Interview
  │   ├── part2/page.tsx       # Long Turn
  │   └── part3/page.tsx       # Discussion
  ├── results/page.tsx         # Results page
  ├── layout.tsx               # Root layout
  └── globals.css              # Global styles

components/
  ├── ProtectedRoute.tsx       # Protected route wrapper
  ├── SpeakingNavbar.tsx       # Navigation bar
  ├── QuestionCard.tsx         # Question display
  ├── MicButton.tsx            # Recording button
  ├── AnswerInput.tsx          # Answer input area
  ├── CircularTimer.tsx        # Countdown timer
  └── LoadingOverlay.tsx       # Loading indicator

context/
  ├── AuthContext.tsx          # Authentication state
  └── TestContext.tsx          # Test results state

lib/
  ├── audio.ts                 # Audio recording utility
  ├── api.ts                   # API utilities
  └── toast.ts                 # Toast notification system
```

## Key Features

### Authentication
- User registration and login with JWT tokens
- Secure token storage in localStorage
- Protected routes with automatic redirect to login
- Token-based API requests

### Speaking Test
- Part 1: Three introduction questions with recording
- Part 2: 60-second preparation + 120-second speaking with circular timer
- Part 3: Three discussion questions with recording
- Real-time audio recording using Web Audio API

### Results
- Overall band score with level classification
- Criterion breakdown (Fluency, Lexical Resource, Grammar, Pronunciation)
- Strengths and areas for improvement
- Improved answer suggestions

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## API Integration

The frontend integrates with the FastAPI backend for:
- User authentication (`/auth/register`, `/auth/token`)
- Question generation (`/generate-part1`, `/generate-part2`, `/generate-part3`)
- Answer evaluation (`/evaluate`)
- Results aggregation (`/aggregate-results`)

All protected endpoints require `Authorization: Bearer <token>` header.

## Development

### Build
```bash
npm run build
```

### Production
```bash
npm start
```

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support with responsive design

## Notes

- The application requires microphone access for voice recording
- Ensure the backend API is running and accessible
- Audio is recorded in WebM format

## License

MIT License - See LICENSE file for details
