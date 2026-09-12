from pydantic import BaseModel


class EventCreate(BaseModel):
    timestamp: str

    file: str
    filesystem_event: str
    event_type: str

    process_name: str
    pid: int
    username: str
    command: str

    threat_score: int
    severity: str
    threat_reasons: list[str]

    # Network attribution from Person A
    source_ip: str | None = None
    source_port: int | None = None
    mac_address: str | None = None
    subnet: str | None = None
    network_type: str | None = None


class EventResponse(BaseModel):
    id: int

    timestamp: str

    file: str
    filesystem_event: str
    event_type: str

    process_name: str
    pid: int
    username: str
    command: str

    threat_score: int
    severity: str
    threat_reasons: list[str]

    # Network attribution
    source_ip: str | None = None
    source_port: int | None = None
    mac_address: str | None = None
    subnet: str | None = None
    network_type: str | None = None

    # Geolocation
    country: str | None = None
    region: str | None = None
    city: str | None = None

    # Response status
    containment_status: str
    process_terminated: str
    ip_blocked: str

    class Config:
        from_attributes = True