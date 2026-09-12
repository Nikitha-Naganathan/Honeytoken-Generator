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


class EventResponse(BaseModel):
    id: int
    timestamp: str
    event_type: str
    file: str
    filesystem_event: str
    pid: int
    process_name: str
    username: str
    command: str
    severity: str

    class Config:
        from_attributes = True