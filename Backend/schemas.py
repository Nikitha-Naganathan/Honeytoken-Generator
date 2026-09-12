from pydantic import BaseModel


class EventCreate(BaseModel):
    timestamp: str
    event_type: str
    file: str
    filesystem_event: str
    pid: int
    process_name: str
    username: str
    command: str
    severity: str
    threat_score: int
    threat_reasons: list[str]


class EventResponse(EventCreate):
    id: int

    class Config:
        from_attributes = True