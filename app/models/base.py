import copy
from typing import Any, List, Optional, Generic, Type, TypeVar

from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


# Think of this like a BaseClass in Rails' Model
# The methods in this class are static methods
class Base(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db_session: Session, id: int) -> Optional[ModelType]:
        return db_session.query(self.model).filter(self.model.id == id).first()

    def get_by(self, db_session: Session, **kwargs) -> Optional[ModelType]:
        return db_session.query(self.model).filter(kwargs).first()

    def where(self, db_session: Session, *args, offset=0, limit=100) -> List[ModelType]:
        q = db_session.query(self.model)
        for arg in args:
            q = q.filter(arg)
        return q.offset(offset).limit(limit).all()

    def create(self, db_session: Session, **kwargs) -> ModelType:
        db_obj = self.model(kwargs)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: Session, db_obj: ModelType, **kwargs) -> ModelType:
        db_obj = jsonable_encoder(db_obj)
        for field in db_obj:
            if field in kwargs:
                setattr(db_obj, field, kwargs[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def remove(self, db_session: Session, db_obj: ModelType) -> ModelType:
        db_session.delete(db_obj)
        db_session.commit()
        return db_obj

    def remove_by_id(self, db_session: Session, id: int) -> ModelType:
        db_obj = self.get(db_session, id)
        return self.remove(db_session, db_obj)
