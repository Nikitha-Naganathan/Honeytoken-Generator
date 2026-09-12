from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
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


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Honeytoken Backend",
    description="Backend for the Deception-Based Endpoint Defense system",
    version="1.0.0"
)


# =========================================================
# CONNECTED WEBSOCKET CLIENTS
# =========================================================

connected_clients = []


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Honeytoken Backend is running!",
        "status": "online"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# POST EVENT
# =========================================================

@app.post("/events", response_model=EventResponse)
async def receive_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. CALCULATE SEVERITY
    # -----------------------------------------------------

    calculated_severity = calculate_severity(
        event_data.file
    )


    # -----------------------------------------------------
    # 2. CHECK ALLOWLIST
    # -----------------------------------------------------

    allowed = is_allowed_process(
        event_data.process_name
    )


    # -----------------------------------------------------
    # 3. NETWORK ATTRIBUTION
    # -----------------------------------------------------
    #
    # IMPORTANT:
    #
    # Person A identifies the source of the suspicious
    # activity and sends it with the event.
    #
    # We therefore DO NOT use request.client.host here.
    #
    # -----------------------------------------------------

    source_ip = event_data.source_ip
    source_port = event_data.source_port
    mac_address = event_data.mac_address
    subnet = event_data.subnet
    network_type = event_data.network_type


    # -----------------------------------------------------
    # 4. IP GEOLOCATION
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
    # 5. INITIAL CONTAINMENT STATE
    # -----------------------------------------------------

    containment_status = "monitoring"

    process_terminated = "not_required"

    ip_blocked = "not_required"


    # -----------------------------------------------------
    # 6. HIGH-CONFIDENCE THREAT RESPONSE
    # -----------------------------------------------------

    if event_data.threat_score >= 80 and not allowed:

        containment_status = "contained"

        # Tell the endpoint agent that the suspicious
        # process should be terminated.
        process_terminated = "requested"

        # Block the attributed source IP in the
        # backend's central response state.
        if source_ip:

            block_ip(source_ip)

            ip_blocked = "blocked"


    # -----------------------------------------------------
    # 7. CREATE DATABASE EVENT
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

        # Network attribution
        source_ip=source_ip,

        source_port=source_port,

        mac_address=mac_address,

        subnet=subnet,

        network_type=network_type,

        # Geolocation
        country=location["country"],

        region=location["region"],

        city=location["city"],

        # Response
        containment_status=containment_status,

        process_terminated=process_terminated,

        ip_blocked=ip_blocked
    )


    # -----------------------------------------------------
    # 8. STORE IN SQLITE
    # -----------------------------------------------------

    db.add(new_event)

    db.commit()

    db.refresh(new_event)


    # -----------------------------------------------------
    # 9. CREATE WEBSOCKET EVENT
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

        # -------------------------------------------------
        # NETWORK INFORMATION
        # -------------------------------------------------

        "source_ip": new_event.source_ip,

        "source_port": new_event.source_port,

        "mac_address": new_event.mac_address,

        "subnet": new_event.subnet,

        "network_type": new_event.network_type,

        # -------------------------------------------------
        # GEOLOCATION
        # -------------------------------------------------

        "country": new_event.country,

        "region": new_event.region,

        "city": new_event.city,

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        "containment_status":
            new_event.containment_status,

        "process_terminated":
            new_event.process_terminated,

        "ip_blocked":
            new_event.ip_blocked
    }


    # -----------------------------------------------------
    # 10. BROADCAST TO DASHBOARD
    # -----------------------------------------------------

    await broadcast_event(
        event_json
    )


    # -----------------------------------------------------
    # 11. DISCORD ALERT
    # -----------------------------------------------------

    if not allowed:

        send_alert(new_event)

    else:

        print(
            f"Allowed process detected: "
            f"{new_event.process_name}"
        )


    # -----------------------------------------------------
    # 12. PRINT CONTAINMENT INFORMATION
    # -----------------------------------------------------

    if containment_status == "contained":

        print(
            "\n========== CONTAINMENT =========="
        )

        print(
            f"Source IP: {source_ip}"
        )

        print(
            f"Source Port: {source_port}"
        )

        print(
            f"MAC Address: {mac_address}"
        )

        print(
            f"Subnet: {subnet}"
        )

        print(
            f"Network Type: {network_type}"
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

        print(
            "=================================\n"
        )


    # -----------------------------------------------------
    # 13. RETURN EVENT
    # -----------------------------------------------------

    return new_event


# =========================================================
# GET ALL EVENTS
# =========================================================

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


# =========================================================
# BLOCK IP
# =========================================================

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


# =========================================================
# UNBLOCK IP
# =========================================================

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


# =========================================================
# GET BLOCKED IPS
# =========================================================

@app.get("/blocked-ips")
def get_blocked():

    return {
        "blocked_ips": get_blocked_ips()
    }


# =========================================================
# CHECK IP
# =========================================================

@app.get("/check-ip/{ip}")
def check_ip(ip: str):

    return {
        "ip": ip,
        "blocked": is_ip_blocked(ip)
    }


# =========================================================
# ISOLATE EVENT
# =========================================================

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


    # Update containment state

    event.containment_status = "isolated"


    # Block source IP if available

    if event.source_ip:

        block_ip(
            event.source_ip
        )

        event.ip_blocked = "blocked"


    db.commit()

    db.refresh(event)


    # -----------------------------------------------------
    # BROADCAST CONTAINMENT UPDATE
    # -----------------------------------------------------

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


# =========================================================
# WEBSOCKET
# =========================================================

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


# =========================================================
# BROADCAST FUNCTION
# =========================================================

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


    # Remove disconnected clients

    for websocket in disconnected_clients:

        if websocket in connected_clients:

            connected_clients.remove(
                websocket
            )