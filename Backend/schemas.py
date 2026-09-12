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

    source_ip: str | None = None


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

    source_ip: str | None
    country: str | None
    region: str | None
    city: str | None

    containment_status: str
    process_terminated: str
    ip_blocked: str

    class Config:
        from_attributes = True