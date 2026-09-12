from pydantic import BaseModel


class EventCreate(BaseModel):
    timestamp: str
    filepath: str
    event_type: str
    process_name: str
    pid: int
    severity: str


class EventResponse(BaseModel):
    id: int
    timestamp: str
    filepath: str
    event_type: str
    process_name: str
    pid: int
    severity: str

    class Config:
        from_attributes = True