from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Session

from app.db.base_class import Base
from app.lib.security import hash_password, verify_password
from app.models.base import Base as ModelBase


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    sessions = relationship("Session", back_populates="user")

# This class is like Rails' Model class. Include methods that  are too complicated
class UserModel(ModelBase[User]):
    def get_by_email(self, db_session: Session, email: str) -> Optional[User]:
        return self.get_by(db_session, {"email": email})

    def authenticate(self, db_session: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create(self, db_session: Session, **kwargs) -> User:
        if "password" in kwargs:
            kwargs["hash_password"] = hash_password(kwargs["password"])
        return self.create(db_session, kwargs)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
