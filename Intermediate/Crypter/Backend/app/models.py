# app/models.py
import uuid
from datetime import datetime  # <-- IMPORT THIS
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.sql import func
from .database import Base

# --- ADD THIS ENTIRE CLASS ---
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_secret_key = Column(String, nullable=False) # This is the S1 key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
# -----------------------------

class Session(Base):
    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    current_round_number = Column(Integer, nullable=False, default=lambda: int(datetime.utcnow().timestamp()))
    user_agent = Column(Text, nullable=True)
    ip_address = Column(INET, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())