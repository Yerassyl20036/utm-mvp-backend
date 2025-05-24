# backend/app/websockets/routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Optional

from app.websockets.connection_manager import manager
from app.deps import get_current_pilot # For WebSocket authentication
from app.models.pilot import Pilot as PilotModel # To avoid conflict with Pydantic schema

websocket_router = APIRouter()

# WebSocket Authentication:
# Simplest way for MVP is to pass token as a query parameter.
# In production, you might use subprotocols or an initial auth message.
async def get_pilot_from_token_query(
    token: Optional[str] = Query(None),
    # db: Session = Depends(get_db) # If you need db for get_current_pilot
    # For this example, get_current_pilot expects the token directly from oauth2_scheme
    # We'll need a modified dependency for websockets if we use get_current_pilot directly
    # For now, let's just identify the connection and handle auth more loosely for MVP broadcast
    # Or, we make `get_current_pilot` more flexible.
    # For simplicity, let's assume a valid token means an authenticated user for now.
    # A more robust solution would involve a custom dependency that extracts and validates the token.
    # current_pilot: PilotModel = Depends(get_current_pilot_ws) # Example of a custom dep
):
    if not token: # For anonymous connections or if auth is handled differently
        return None
    # Here you would typically decode and validate the token to get the pilot
    # For MVP, we're keeping it simpler. If a token is passed, we assume it's for a logged-in user.
    # In a real app, you'd use a dependency like `get_current_pilot` but adapted for WS.
    # For instance, by creating a `get_current_pilot_ws` that takes the token string.
    # from app.core import security
    # from app import crud
    # payload = security.decode_access_token(token)
    # if not payload or not (email := payload.get("sub")):
    #     return None
    # pilot = crud.get_pilot_by_email(db, email=email)
    # return pilot
    return {"token": token} # Placeholder for authenticated user identifier


@websocket_router.websocket("/ws/telemetry")
async def telemetry_websocket_endpoint(
    websocket: WebSocket,
    # For MVP, let's not enforce strict auth on connect for simplicity of broadcast,
    # but client should send token if it wants personalized data later.
    # Or, we can make token mandatory.
    token: Optional[str] = Query(None) # Pilot's auth token
):
    client_id = "anonymous"
    if token:
        # Here you would normally validate the token and get the pilot_id
        # For MVP, we'll just use the token (or part of it) as a pseudo client_id
        # In a real app, use a proper user identification method.
        # pilot = await get_pilot_from_token_query(token) # This would be an async dep
        # if pilot:
        #     client_id = str(pilot.id) # Example
        client_id = f"user_with_token_ending_{token[-5:]}" if len(token or "") >=5 else "user_with_token"


    await manager.connect(websocket, client_id=client_id)
    try:
        while True:
            # For now, this websocket is primarily for receiving broadcasts.
            # We can add logic to handle messages sent from client to server if needed.
            data = await websocket.receive_text()
            # Example: if client sends a message
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
            print(f"Message received from {client_id}: {data} (not processed further)")
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id=client_id)
    except Exception as e:
        print(f"Error in WebSocket connection for {client_id}: {e}")
        manager.disconnect(websocket, client_id=client_id) # Ensure disconnect on other errors