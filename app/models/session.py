from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session

from app.db.base_class import Base
from app.lib.security import hash_password, verify_password
from app.models.base import Base as ModelBase


class Session(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user = relationship("User", back_populates="sessions")
    ip_address = Column(String)
    user_agent = Column(String)
    last_accessed_at = Column(DateTime)

class SessionModel(ModelBase[User]):
    pass
