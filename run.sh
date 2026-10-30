#!/usr/bin/env bash
# Quick Start Script for potatoGuardProject

echo "=========================================================="
echo "🥔 potatoGuardProject — Potato Leaf Disease Classifier"
echo "=========================================================="
echo "Starting FastAPI Production Web Server on http://localhost:8000"
echo "To run Streamlit instead: streamlit run streamlit_app.py"
echo "=========================================================="

python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

