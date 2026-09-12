from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from database import Base
from models import Event
from schemas import EventCreate, EventResponse
from severity import calculate_severity
from alerts import send_alert
from allowlist import is_allowed_process


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Honeytoken Backend",
    description="Backend for the Deception-Based Endpoint Defense system",
    version="1.0.0"
)


# Connected WebSocket clients
connected_clients = []


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Honeytoken Backend is running!",
        "status": "online"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# POST EVENT
# ---------------------------------------------------------

@app.post("/events", response_model=EventResponse)
async def receive_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. Calculate severity
    # -----------------------------------------------------

    calculated_severity = calculate_severity(
        event_data.file
    )


    # -----------------------------------------------------
    # 2. Check allowlist
    # -----------------------------------------------------

    allowed = is_allowed_process(
        event_data.process_name
    )


    # -----------------------------------------------------
    # 3. Create database event
    # -----------------------------------------------------

    new_event = Event(
        timestamp=event_data.timestamp,
        event_type=event_data.event_type,
        file=event_data.file,
        filesystem_event=event_data.filesystem_event,
        pid=event_data.pid,
        process_name=event_data.process_name,
        username=event_data.username,
        command=event_data.command,
        severity=calculated_severity
    )


    # -----------------------------------------------------
    # 4. Store in SQLite
    # -----------------------------------------------------

    db.add(new_event)
    db.commit()
    db.refresh(new_event)


    # -----------------------------------------------------
    # 5. Convert event into dictionary
    #    for WebSocket clients
    # -----------------------------------------------------

    event_json = {
        "id": new_event.id,
        "timestamp": new_event.timestamp,
        "event_type": new_event.event_type,
        "file": new_event.file,
        "filesystem_event": new_event.filesystem_event,
        "pid": new_event.pid,
        "process_name": new_event.process_name,
        "username": new_event.username,
        "command": new_event.command,
        "severity": new_event.severity,
        "allowed": allowed
    }


    # -----------------------------------------------------
    # 6. Broadcast event to dashboard
    # -----------------------------------------------------

    await broadcast_event(event_json)


    # -----------------------------------------------------
    # 7. Send Discord alert if process is NOT allowed
    # -----------------------------------------------------

    if not allowed:
        send_alert(new_event)
    else:
        print(
            f"Allowed process detected: "
            f"{new_event.process_name}"
        )


    # -----------------------------------------------------
    # 8. Return event to API caller
    # -----------------------------------------------------

    return new_event


# ---------------------------------------------------------
# GET ALL EVENTS
# ---------------------------------------------------------

@app.get("/events")
def get_events(
    db: Session = Depends(get_db)
):

    events = (
        db.query(Event)
        .order_by(Event.id.desc())
        .all()
    )

    return events


# ---------------------------------------------------------
# WEBSOCKET
# ---------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    connected_clients.append(websocket)

    print(
        f"WebSocket client connected. "
        f"Total clients: {len(connected_clients)}"
    )

    try:

        while True:

            # Keep connection alive
            await websocket.receive_text()

    except WebSocketDisconnect:

        if websocket in connected_clients:
            connected_clients.remove(websocket)

        print(
            f"WebSocket client disconnected. "
            f"Total clients: {len(connected_clients)}"
        )


# ---------------------------------------------------------
# BROADCAST FUNCTION
# ---------------------------------------------------------

async def broadcast_event(event):

    disconnected_clients = []

    for websocket in connected_clients:

        try:

            await websocket.send_json(event)

        except Exception:

            disconnected_clients.append(websocket)


    # Remove dead connections
    for websocket in disconnected_clients:

        if websocket in connected_clients:
            connected_clients.remove(websocket)