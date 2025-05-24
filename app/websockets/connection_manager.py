# backend/app/websockets/connection_manager.py
from fastapi import WebSocket
from typing import List, Dict, Optional
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections, perhaps keyed by user_id or flight_id if filtering is needed
        # For MVP, a simple list of all connections is fine.
        self.active_connections: List[WebSocket] = []
        # If you want to associate connections with users/flights:
        # self.active_connections_map: Dict[str, List[WebSocket]] = {} # e.g. str could be user_id

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        # if client_id:
        #     if client_id not in self.active_connections_map:
        #         self.active_connections_map[client_id] = []
        #     self.active_connections_map[client_id].append(websocket)
        print(f"Client {client_id or 'anonymous'} connected. Total connections: {len(self.active_connections)}")


    def disconnect(self, websocket: WebSocket, client_id: Optional[str] = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        # if client_id and client_id in self.active_connections_map:
        #     if websocket in self.active_connections_map[client_id]:
        #         self.active_connections_map[client_id].remove(websocket)
        #     if not self.active_connections_map[client_id]: # remove client_id if no connections left
        #         del self.active_connections_map[client_id]
        print(f"Client {client_id or 'anonymous'} disconnected. Total connections: {len(self.active_connections)}")


    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str): # Broadcast to all
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to a client: {e}. Removing stale connection.")
                # Attempt to remove stale connection, though disconnect should handle it
                if connection in self.active_connections:
                     self.active_connections.remove(connection)


    async def broadcast_json(self, data: dict):
        await self.broadcast(json.dumps(data))

    # If you implement per-client or per-group messaging:
    # async def broadcast_to_client(self, message: str, client_id: str):
    #     if client_id in self.active_connections_map:
    #         for connection in self.active_connections_map[client_id]:
    #             await connection.send_text(message)

manager = ConnectionManager() # Singleton instance