from fastapi import FastAPI

from backend.api.routes.users import router as user_router
from backend.api.routes.conversations import router as conversation_router

from backend.modules.core.robot_brain import RobotBrain

app = FastAPI(
    title="AI Assistant Robot",
    description="Backend API for AI Assistant Robot",
    version="1.0.0",
)

# Initialize Robot Brain
brain = RobotBrain()
brain.startup()

# Include API Routes
app.include_router(user_router)
app.include_router(conversation_router)


@app.get("/")
async def root():
    return {
        "message": "AI Assistant Robot Backend Running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }


@app.get("/status")
async def status():
    return brain.get_status()