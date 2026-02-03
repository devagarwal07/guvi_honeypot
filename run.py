"""
Production startup script
Runs the FastAPI application with proper configuration
"""
import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )
