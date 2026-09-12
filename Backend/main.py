from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request
from sqlalchemy.orm import Session

from database import engine, get_db
from database import Base
from models import Event
from schemas import EventCreate, EventResponse
from severity import calculate_severity
from alerts import send_alert
from allowlist import is_allowed_process

from ip_geolocation import get_ip_location
from blocked_ips import (
    block_ip,
    unblock_ip,
    is_ip_blocked,
    get_blocked_ips
)


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
    request: Request,
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
    # 3. Identify source IP
    # -----------------------------------------------------

    source_ip = (
        request.client.host
        if request.client
        else None
    )


    # -----------------------------------------------------
    # 4. IP geolocation
    # -----------------------------------------------------

    if source_ip:
        location = get_ip_location(source_ip)
    else:
        location = {
            "country": "Unknown",
            "region": "Unknown",
            "city": "Unknown"
        }


    # -----------------------------------------------------
    # 5. Determine initial containment state
    # -----------------------------------------------------

    containment_status = "monitoring"
    process_terminated = "not_required"
    ip_blocked = "not_required"


    # High-confidence event
    if event_data.threat_score >= 80 and not allowed:

        containment_status = "contained"

        # B records that endpoint process termination
        # should happen.
        process_terminated = "requested"


        # Block the source IP when available
        if source_ip:

            block_ip(source_ip)

            ip_blocked = "blocked"


    # -----------------------------------------------------
    # 6. Create database event
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

        threat_score=event_data.threat_score,

        severity=calculated_severity,

        threat_reasons=event_data.threat_reasons,

        source_ip=source_ip,

        country=location["country"],

        region=location["region"],

        city=location["city"],

        containment_status=containment_status,

        process_terminated=process_terminated,

        ip_blocked=ip_blocked
    )


    # -----------------------------------------------------
    # 7. Store in SQLite
    # -----------------------------------------------------

    db.add(new_event)

    db.commit()

    db.refresh(new_event)


    # -----------------------------------------------------
    # 8. Convert event into dictionary
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

        "threat_score": new_event.threat_score,

        "threat_reasons": new_event.threat_reasons,

        "allowed": allowed,

        # Source information
        "source_ip": new_event.source_ip,

        "country": new_event.country,

        "region": new_event.region,

        "city": new_event.city,

        # Response information
        "containment_status": new_event.containment_status,

        "process_terminated": new_event.process_terminated,

        "ip_blocked": new_event.ip_blocked
    }


    # -----------------------------------------------------
    # 9. Broadcast event to dashboard
    # -----------------------------------------------------

    await broadcast_event(event_json)


    # -----------------------------------------------------
    # 10. Send Discord alert
    # -----------------------------------------------------

    if not allowed:

        send_alert(new_event)

    else:

        print(
            f"Allowed process detected: "
            f"{new_event.process_name}"
        )


    # -----------------------------------------------------
    # 11. Print containment information
    # -----------------------------------------------------

    if containment_status == "contained":

        print("\n========== CONTAINMENT ==========")

        print(
            f"Source IP: {source_ip}"
        )

        print(
            f"Location: "
            f"{location['city']}, "
            f"{location['region']}, "
            f"{location['country']}"
        )

        print(
            f"Process: "
            f"{event_data.process_name}"
        )

        print(
            f"PID: "
            f"{event_data.pid}"
        )

        print(
            f"Process termination: "
            f"{process_terminated}"
        )

        print(
            f"IP status: "
            f"{ip_blocked}"
        )

        print(
            f"Containment: "
            f"{containment_status}"
        )

        print("=================================\n")


    # -----------------------------------------------------
    # 12. Return event
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
# BLOCK IP
# ---------------------------------------------------------

@app.post("/block-ip/{ip}")
async def block_ip_endpoint(
    ip: str
):

    block_ip(ip)

    result = {
        "ip": ip,
        "status": "blocked"
    }

    await broadcast_event({
        "type": "ip_block",
        **result
    })

    return result


# ---------------------------------------------------------
# UNBLOCK IP
# ---------------------------------------------------------

@app.post("/unblock-ip/{ip}")
async def unblock_ip_endpoint(
    ip: str
):

    unblock_ip(ip)

    result = {
        "ip": ip,
        "status": "unblocked"
    }

    await broadcast_event({
        "type": "ip_unblock",
        **result
    })

    return result


# ---------------------------------------------------------
# GET BLOCKED IPs
# ---------------------------------------------------------

@app.get("/blocked-ips")
def get_blocked():

    return {
        "blocked_ips": get_blocked_ips()
    }


# ---------------------------------------------------------
# CHECK IP
# ---------------------------------------------------------

@app.get("/check-ip/{ip}")
def check_ip(ip: str):

    return {
        "ip": ip,
        "blocked": is_ip_blocked(ip)
    }


# ---------------------------------------------------------
# ISOLATE EVENT
# ---------------------------------------------------------

@app.post("/isolate/{event_id}")
async def isolate_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )


    if not event:

        return {
            "error": "Event not found"
        }


    event.containment_status = "isolated"


    if event.source_ip:

        block_ip(event.source_ip)

        event.ip_blocked = "blocked"


    db.commit()

    db.refresh(event)


    isolation_message = {

        "type": "containment_update",

        "event_id": event.id,

        "containment_status":
            event.containment_status,

        "source_ip":
            event.source_ip,

        "ip_blocked":
            event.ip_blocked
    }


    await broadcast_event(
        isolation_message
    )


    return isolation_message


# ---------------------------------------------------------
# WEBSOCKET
# ---------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    connected_clients.append(
        websocket
    )

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

            connected_clients.remove(
                websocket
            )

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

            await websocket.send_json(
                event
            )

        except Exception:

            disconnected_clients.append(
                websocket
            )


    # Remove dead connections

    for websocket in disconnected_clients:

        if websocket in connected_clients:

            connected_clients.remove(
                websocket
            )