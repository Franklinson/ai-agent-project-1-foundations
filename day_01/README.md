# Day 1: Development Environment and REST API

## Overview

Day 1 focuses on setting up a professional development environment and building your first REST API endpoint that an AI agent could interact with.

## Files

- `config.py`: Environment variable configuration
- `main.py`: FastAPI application with REST endpoints
- `test_api.py`: API testing script
- `test_config.py`: Configuration testing script

## Running the API

```bash
# Activate virtual environment
source ../.venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run the API server
uvicorn main:app --reload

# API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs