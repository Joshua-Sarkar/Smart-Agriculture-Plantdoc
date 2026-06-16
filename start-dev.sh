#!/bin/bash
# PlantDoc Quick Start Script

echo "🍃 PlantDoc - Starting development environment"
echo ""

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

echo "✓ Prerequisites checked"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "✓ Backend dependencies installed"

# Start backend in background
echo "🚀 Starting FastAPI server..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✓ Backend running (PID: $BACKEND_PID)"
echo ""

# Frontend setup
cd ../frontend
echo "📦 Setting up frontend..."
if [ ! -d "node_modules" ]; then
    npm install -q
    echo "✓ Frontend dependencies installed"
fi

echo "🚀 Starting Vite dev server..."
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
