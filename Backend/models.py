from sqlalchemy import Column, Integer, String, JSON
from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(String, nullable=False)
    file = Column(String, nullable=False)
    filesystem_event = Column(String, nullable=False)
    event_type = Column(String, nullable=False)

    process_name = Column(String, nullable=False)
    pid = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    command = Column(String, nullable=False)

    threat_score = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    threat_reasons = Column(JSON, nullable=False)

    source_ip = Column(String, nullable=True)
    country = Column(String, nullable=True)
    region = Column(String, nullable=True)
    city = Column(String, nullable=True)

    containment_status = Column(String, default="detected")
    process_terminated = Column(String, default="pending")
    ip_blocked = Column(String, default="pending")