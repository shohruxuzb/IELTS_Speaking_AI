# IELTS Speaking AI - Setup Guide

This document provides step-by-step instructions for setting up the IELTS Speaking AI application with both frontend (Next.js) and backend (FastAPI).

## Backend Setup (FastAPI)

### Prerequisites
- Python 3.10+
- pip or uv package manager

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
# or using uv:
uv pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create a .env file in the root directory
cp .env.example .env

# Update .env with your configuration:
# - GROQ_API_KEY: Your Groq API key for AI evaluation
# - JWT_SECRET_KEY: A secure random string for JWT signing
# - REDIS_URL: Redis connection URL (optional, for caching)
# - SUPABASE_URL & SUPABASE_KEY: Supabase credentials (optional)
```

3. Run the FastAPI backend:
```bash
python main.py
# or using uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Frontend Setup (Next.js)

### Prerequisites
- Node.js 18+ 
- npm, yarn, pnpm, or bun

### Installation

1. Install dependencies:
```bash
npm install
# or
pnpm install
```

2. Create environment file:
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

3. Run the development server:
```bash
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`

### Environment Variables

#### Development
- `NEXT_PUBLIC_API_URL=http://localhost:8000`

#### Production (Vercel/Deployed)
- `NEXT_PUBLIC_API_URL=https://your-backend-domain.com`

## Full Stack Testing

1. **Start Backend**:
   ```bash
   # Terminal 1
   python main.py
   ```

2. **Start Frontend**:
   ```bash
   # Terminal 2
   npm run dev
   ```

3. **Open Browser**:
   ```
   http://localhost:3000
   ```

4. **Test Registration & Login**:
   - Click "Get Started" on landing page
   - Register a new account
   - Login with credentials
   - Navigate to Part 1 of speaking test

## Troubleshooting

### "Failed to fetch" error
- **Cause**: Backend is not running or API URL is incorrect
- **Solution**: 
  1. Verify backend is running: `http://localhost:8000/docs`
  2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
  3. Check browser console for detailed error messages (use F12)

### CORS errors
- **Cause**: Backend CORS middleware not configured for frontend origin
- **Solution**: 
  1. Verify CORS middleware is added to `main.py`
  2. Ensure your frontend URL is in the `allow_origins` list

### API returns 401 Unauthorized
- **Cause**: Invalid or expired JWT token
- **Solution**:
  1. Clear browser localStorage: `localStorage.clear()`
  2. Logout and login again
  3. Check `JWT_SECRET_KEY` matches between frontend and backend

### Groq API errors during evaluation
- **Cause**: Missing or invalid `GROQ_API_KEY`
- **Solution**:
  1. Set `GROQ_API_KEY` in backend `.env` file
  2. Restart the backend server
  3. Try evaluation again

## Development Tips

- **Frontend Debug Logs**: Check browser console (F12) for `[v0]` prefixed logs
- **Backend Debug Logs**: Check terminal output for detailed error messages
- **Hot Reload**: Frontend supports hot module replacement (HMR)
- **API Testing**: Use Swagger UI at `http://localhost:8000/docs`

## Deployment

### Frontend (Vercel)
1. Connect GitHub repository to Vercel
2. Set `NEXT_PUBLIC_API_URL` to your production backend URL
3. Deploy automatically on push

### Backend (Vercel/Railway/Heroku)
1. Update `NEXT_PUBLIC_API_URL` in frontend `.env.local` or Vercel dashboard
2. Ensure backend CORS allows your frontend domain
3. Deploy and test authentication flow

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq API Documentation](https://console.groq.com)
- [JWT (JSON Web Tokens)](https://jwt.io/)
