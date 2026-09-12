from sqlalchemy import Column, Integer, String, JSON

from database import Base


class Event(Base):
    __tablename__ = "events"

    # ---------------------------------------------------------
    # BASIC EVENT INFORMATION
    # ---------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp = Column(
        String,
        nullable=False
    )

    file = Column(
        String,
        nullable=False
    )

    filesystem_event = Column(
        String,
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    # ---------------------------------------------------------
    # PROCESS INFORMATION
    # ---------------------------------------------------------

    process_name = Column(
        String,
        nullable=False
    )

    pid = Column(
        Integer,
        nullable=False
    )

    username = Column(
        String,
        nullable=False
    )

    command = Column(
        String,
        nullable=False
    )

    # ---------------------------------------------------------
    # THREAT INFORMATION
    # ---------------------------------------------------------

    threat_score = Column(
        Integer,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    threat_reasons = Column(
        JSON,
        nullable=False
    )

    # ---------------------------------------------------------
    # NETWORK ATTRIBUTION
    # ---------------------------------------------------------

    source_ip = Column(
        String,
        nullable=True
    )

    source_port = Column(
        Integer,
        nullable=True
    )

    mac_address = Column(
        String,
        nullable=True
    )

    subnet = Column(
        String,
        nullable=True
    )

    network_type = Column(
        String,
        nullable=True
    )

    # ---------------------------------------------------------
    # GEOLOCATION
    # ---------------------------------------------------------

    country = Column(
        String,
        nullable=True
    )

    region = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=True
    )

    # ---------------------------------------------------------
    # RESPONSE / CONTAINMENT
    # ---------------------------------------------------------

    containment_status = Column(
        String,
        default="detected"
    )

    process_terminated = Column(
        String,
        default="pending"
    )

    ip_blocked = Column(
        String,
        default="pending"
    )