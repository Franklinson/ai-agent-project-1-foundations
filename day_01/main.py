"""
FastAPI application for Day 1.

This API demonstrates REST endpoints that an AI agent could interact with.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_01.config import config

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    description="REST API for AI Agent interactions - Day 1",
    version="1.0.0",
    debug=config.DEBUG
)

# In-memory storage for tasks (use database in production)
tasks_db: List[dict] = []
next_task_id = 1

# Pydantic models for request/response validation
class TaskCreate(BaseModel):
    """Request model for creating a task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    priority: Optional[str] = Field("medium", description="Task priority: low, medium, high")
    due_date: Optional[str] = Field(None, description="Due date in ISO format (YYYY-MM-DD)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "priority": "high",
                "due_date": "2024-01-15"
            }
        }

class TaskResponse(BaseModel):
    """Response model for task data."""
    id: int
    title: str
    priority: str
    status: str
    due_date: Optional[str]
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "priority": "high",
                "status": "created",
                "due_date": "2024-01-15",
                "created_at": "2024-01-10T10:00:00Z"
            }
        }

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    app_name: str
    version: str

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to AI Agent Project 1 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Agents can use this to verify the API is running and accessible.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        app_name=config.APP_NAME,
        version="1.0.0"
    )

@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """
    Create a new task.
    
    This is a tool endpoint that an AI agent could call to create tasks.
    The agent would use this endpoint when it decides a task needs to be created.
    
    Example agent usage:
    - Agent receives: "Please create a task to buy groceries"
    - Agent calls: POST /api/tasks with {"title": "Buy groceries", "priority": "medium"}
    - Agent receives: Task created with ID 1
    - Agent confirms: "I've created task #1: Buy groceries"
    """
    global next_task_id
    
    # Validate priority
    valid_priorities = ["low", "medium", "high"]
    if task.priority not in valid_priorities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Priority must be one of: {', '.join(valid_priorities)}"
        )
    
    # Validate due_date format if provided
    if task.due_date:
        try:
            datetime.strptime(task.due_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="due_date must be in YYYY-MM-DD format"
            )
    
    # Create task
    new_task = {
        "id": next_task_id,
        "title": task.title,
        "priority": task.priority,
        "status": "created",
        "due_date": task.due_date,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    tasks_db.append(new_task)
    next_task_id += 1
    
    return TaskResponse(**new_task)

@app.get("/api/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(status_filter: Optional[str] = None):
    """
    List all tasks, optionally filtered by status.
    
    Agents can use this to retrieve task information.
    """
    if status_filter:
        filtered_tasks = [t for t in tasks_db if t["status"] == status_filter]
        return [TaskResponse(**task) for task in filtered_tasks]
    
    return [TaskResponse(**task) for task in tasks_db]

@app.get("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(task_id: int):
    """
    Get a specific task by ID.
    
    Agents can use this to retrieve details about a specific task.
    """
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return TaskResponse(**task)

@app.patch("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task_status(task_id: int, status: str):
    """
    Update a task's status.
    
    Agents can use this to mark tasks as completed or change their status.
    """
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    valid_statuses = ["created", "in_progress", "completed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    task["status"] = status
    task["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return TaskResponse(**task)

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url)
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
