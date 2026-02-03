"""
FastAPI entry point for Agentic Honey-Pot Scam Detection System
Handles incoming message events and orchestrates scam detection + agent engagement
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import uvicorn
import logging

from auth import verify_api_key
from config import settings
from detector.scam_classifier import ScamClassifier
from agent.agent_controller import AgentController
from extractor.intelligence import IntelligenceExtractor
from sessions.memory_store import SessionMemoryStore
from callbacks.guvi_client import GuviCallbackClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentic Honey-Pot API", version="1.0.0")

# Initialize components
scam_classifier = ScamClassifier()
agent_controller = AgentController()
intelligence_extractor = IntelligenceExtractor()
session_store = SessionMemoryStore()
callback_client = GuviCallbackClient()


# Request/Response Models
class Message(BaseModel):
    sender: Literal["scammer", "user"]
    text: str
    timestamp: int


class Metadata(BaseModel):
    channel: Literal["SMS", "WhatsApp", "Email", "Chat"]
    language: str
    locale: str


class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = Field(default_factory=list)
    metadata: Metadata


class ApiResponse(BaseModel):
    status: str
    reply: str


@app.post("/api/message", response_model=ApiResponse)
async def handle_message(
    request: IncomingRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Main endpoint to receive suspected scam messages
    Processes each message and returns a human-like reply
    """
    try:
        session_id = request.sessionId
        incoming_message = request.message
        conversation_history = request.conversationHistory
        metadata = request.metadata
        
        logger.info(f"Processing message for session: {session_id}")
        
        # Get or create session state
        session = session_store.get_or_create_session(session_id)
        
        # Increment message counter
        session_store.increment_message_count(session_id)
        
        # Build full conversation context - convert Pydantic models to dicts
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
                logger.info(f"Scam detected for session: {session_id}")
                session_store.mark_scam_detected(session_id)
                session.scam_detected = True
        
        # Generate reply based on scam detection status
        if session.scam_detected:
            # Use AI agent to generate human-like reply
            reply = agent_controller.generate_reply(
                incoming_message.text,
                full_history,
                session_id,
                metadata
            )
            
            # Extract intelligence from the incoming message
            extracted = intelligence_extractor.extract_from_message(incoming_message.text)
            session_store.add_intelligence(session_id, extracted)
            
            # Check if engagement should end
            should_end = agent_controller.should_end_engagement(
                session.total_messages,
                session.intelligence,
                full_history
            )
            
            if should_end and not session.callback_sent:
                # Send final callback to evaluation endpoint
                logger.info(f"Sending final callback for session: {session_id}")
                callback_success = await callback_client.send_final_result(
                    session_id=session_id,
                    scam_detected=True,
                    total_messages=session.total_messages,
                    intelligence=session.intelligence,
                    conversation_history=full_history
                )
                
                if callback_success:
                    session_store.mark_callback_sent(session_id)
                    logger.info(f"Callback sent successfully for session: {session_id}")
                else:
                    logger.error(f"Failed to send callback for session: {session_id}")
        else:
            # Normal conversation - respond naturally without revealing detection
            reply = agent_controller.generate_normal_reply(
                incoming_message.text,
                full_history,
                metadata
            )
        
        # Store the conversation turn
        session_store.add_conversation_turn(session_id, incoming_message, reply)
        
        return ApiResponse(status="success", reply=reply)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        # Return a safe generic response even on error
        return ApiResponse(
            status="success",
            reply="Sorry, I didn't quite understand. Could you explain again?"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "honeypot-api"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
