from typing import List
from sqlalchemy.orm import Session, Query

from data.database import Base


class CONTROLLER:
    def __init__(self, db_session: Session, db_model: Base):
        self.db_session = db_session
        self.db_model = db_model

    def get(self, model_id: int) -> Base:
        return (
            self.db_session.query(self.db_model)
            .filter(self.db_model.id == model_id)
            .first()
        )

    def get_all(self) -> List[Base]:
        return self.db_session.query(self.db_model).all()

    def create(self, model_schema) -> Base:
        new_register = self.db_model(**model_schema.dict())
        self.db_session.add(new_register)
        self.db_session.commit()
        self.db_session.refresh(new_register)
        return new_register

    def update(self, model_id: int, model_schema) -> Base:
        self.db_session.query(self.db_model).filter(
            self.db_model.id == model_id
        ).update(model_schema.dict(exclude_unset=True), synchronize_session="evaluate")
        self.db_session.commit()
        return self.get(model_id)

    def delete(self, model_id: int):
        entity = self.get(model_id)
        self.db_session.delete(entity)
        self.db_session.commit()
