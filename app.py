"""
FastAPI entry point for Agentic Honey-Pot Scam Detection System
Handles incoming message events and orchestrates scam detection + agent engagement
OPTIMIZED FOR LOW LATENCY - Avoids timeouts on Render free tier
"""
from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Literal
import uvicorn
import logging
import asyncio

from auth import verify_api_key
from config import settings
from detector.scam_classifier import ScamClassifier
from agent.agent_controller import AgentController
from extractor.intelligence import IntelligenceExtractor
from sessions.memory_store import SessionMemoryStore
from callbacks.guvi_client import GuviCallbackClient

# Configure logging - minimal for production
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentic Honey-Pot API", version="1.0.0")

# Initialize components (lightweight - no heavy initialization)
scam_classifier = ScamClassifier()
agent_controller = AgentController()
intelligence_extractor = IntelligenceExtractor()
session_store = SessionMemoryStore()
callback_client = GuviCallbackClient()


@app.on_event("startup")
async def startup_event():
    """Pre-warm the application on startup"""
    # Pre-compile regex patterns if any
    pass


@app.get("/health")
async def health_check():
    """Health check endpoint - fast response"""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint - fast response"""
    return {"status": "ok", "service": "honeypot-api"}


# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid request format",
            "details": exc.errors()
        }
    )


# Request/Response Models
class Message(BaseModel):
    sender: str  # Changed from Literal to accept any string
    text: str
    timestamp: int


class Metadata(BaseModel):
    channel: str = "SMS"  # Made optional with default
    language: str = "English"  # Made optional with default
    locale: str = "IN"  # Made optional with default


class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = Field(default_factory=list)
    metadata: Metadata = Field(default_factory=Metadata)  # Use default factory instead of Optional


class ApiResponse(BaseModel):
    status: str
    reply: str


@app.post("/api/message", response_model=ApiResponse)
async def handle_message(
    request: IncomingRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Main endpoint to receive suspected scam messages
    Processes each message and returns a human-like reply
    OPTIMIZED: Uses fast rule-based responses with LLM as fallback
    """
    try:
        session_id = request.sessionId
        incoming_message = request.message
        conversation_history = request.conversationHistory
        metadata = request.metadata
        
        # Get or create session state
        session = session_store.get_or_create_session(session_id)
        
        # Increment message counter
        session_store.increment_message_count(session_id)
        
        # Build full conversation context
        full_history = [
            {"sender": msg.sender, "text": msg.text, "timestamp": msg.timestamp}
            for msg in conversation_history
        ] + [
            {"sender": incoming_message.sender, "text": incoming_message.text, "timestamp": incoming_message.timestamp}
        ]
        
        # Detect scam intent if not already detected
        if not session.scam_detected:
            scam_detected = scam_classifier.detect_scam(
                incoming_message.text,
                full_history,
                metadata
            )
            
            if scam_detected:
                session_store.mark_scam_detected(session_id)
                session.scam_detected = True
        
        # Generate reply - FAST PATH FIRST
        if session.scam_detected:
            # Use FAST rule-based reply first, LLM only if needed
            reply = agent_controller.generate_fast_reply(
                incoming_message.text,
                full_history,
                session_id
            )
            
            # Extract intelligence from the incoming message (fast regex)
            extracted = intelligence_extractor.extract_from_message(incoming_message.text)
            session_store.add_intelligence(session_id, extracted)
            
            # Check if engagement should end
            should_end = agent_controller.should_end_engagement(
                session.total_messages,
                session.intelligence,
                full_history
            )
            
            if should_end and not session.callback_sent:
                # Send callback in BACKGROUND to not block response
                background_tasks.add_task(
                    send_callback_background,
                    session_id,
                    session.total_messages,
                    session.intelligence,
                    full_history
                )
                session_store.mark_callback_sent(session_id)
        else:
            # Normal cautious response
            reply = agent_controller.generate_fast_reply(
                incoming_message.text,
                full_history,
                session_id
            )
        
        # Store conversation turn
        session_store.add_conversation_turn(session_id, incoming_message, reply)
        
        return ApiResponse(status="success", reply=reply)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        # Return safe generic response even on error
        return ApiResponse(
            status="success",
            reply="I didn't understand. Can you explain again?"
        )


async def send_callback_background(session_id: str, total_messages: int, intelligence: dict, history: list):
    """Background task to send callback without blocking response"""
    try:
        await callback_client.send_final_result(
            session_id=session_id,
            scam_detected=True,
            total_messages=total_messages,
            intelligence=intelligence,
            conversation_history=history
        )
    except Exception as e:
        logger.error(f"Callback error: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
