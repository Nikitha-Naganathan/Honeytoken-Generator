from sqlalchemy import Column, Integer, String
from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    event_type = Column(String, nullable=False)

    process_name = Column(String, nullable=False)
    pid = Column(Integer, nullable=False)

    severity = Column(String, nullable=False)